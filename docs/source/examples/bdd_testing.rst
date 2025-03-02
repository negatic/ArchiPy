.. _examples_bdd:

BDD Testing with ArchiPy
=======================

ArchiPy provides comprehensive support for Behavior-Driven Development testing using Behave.

Feature File Example
------------------

.. code-block:: gherkin

    # features/user_management.feature
    Feature: User Management

      Background:
        Given the application database is initialized

      Scenario: Create a new user
        When a new user "John Doe" with email "john@example.com" is created
        Then the user should exist in the database
        And the user should have the correct email "john@example.com"

      @async
      Scenario: Retrieve user asynchronously
        Given a user with email "jane@example.com" exists
        When I retrieve the user by email asynchronously
        Then the user details should be retrieved successfully

Environment Setup
---------------

ArchiPy's BDD framework uses scenario context isolation and pooling:

.. code-block:: python

    # features/environment.py
    import logging
    import uuid
    from behave.model import Scenario
    from behave.runner import Context

    from archipy.configs.base_config import BaseConfig
    from features.scenario_context_pool_manager import ScenarioContextPoolManager

    # Define test configuration
    class TestConfig(BaseConfig):
        # Test-specific configurations
        SQLALCHEMY = {
            "DRIVER_NAME": "sqlite",
            "DATABASE": ":memory:",
            "ISOLATION_LEVEL": None
        }

    def before_all(context: Context):
        """Setup performed once at the start of the test run."""
        # Set up logging
        context.logger = logging.getLogger("behave")

        # Create scenario context pool
        context.scenario_context_pool = ScenarioContextPoolManager()

        # Set global configuration for tests
        config = TestConfig()
        BaseConfig.set_global(config)

        context.logger.info("Test environment initialized")

    def before_scenario(context: Context, scenario: Scenario):
        """Setup performed before each scenario."""
        # Generate unique ID for scenario
        scenario_id = uuid.uuid4()
        scenario.id = scenario_id

        # Get isolated context for this scenario
        scenario_context = context.scenario_context_pool.get_context(scenario_id)
        scenario_context.store("test_config", BaseConfig.global_config())

        context.logger.info(f"Preparing scenario: {scenario.name} (ID: {scenario_id})")

    def after_scenario(context: Context, scenario: Scenario):
        """Cleanup performed after each scenario."""
        # Get the scenario ID
        scenario_id = getattr(scenario, "id", "unknown")
        context.logger.info(f"Cleaning up scenario: {scenario.name} (ID: {scenario_id})")

        # Clean up the scenario context
        if hasattr(context, "scenario_context_pool"):
            context.scenario_context_pool.cleanup_context(scenario_id)

Scenario Context Management
-------------------------

Create a scenario context to isolate test state:

.. code-block:: python

    # features/scenario_context.py
    class ScenarioContext:
        """A storage class for scenario-specific objects."""

        def __init__(self, scenario_id):
            """Initialize with a unique scenario ID."""
            self.scenario_id = scenario_id
            self.storage = {}
            self.db_file = None
            self.adapter = None
            self.async_adapter = None
            self.entities = {}

        def store(self, key, value):
            """Store a value in the context."""
            self.storage[key] = value

        def get(self, key, default=None):
            """Get a value from the context."""
            return self.storage.get(key, default)

        def cleanup(self):
            """Clean up resources used by this context."""
            if self.adapter:
                try:
                    self.adapter.session_manager.remove_session()
                except Exception as e:
                    print(f"Error in cleanup: {e}")

            # Handle async resources too
            if self.async_adapter:
                import asyncio
                try:
                    temp_loop = asyncio.new_event_loop()
                    try:
                        asyncio.set_event_loop(temp_loop)
                        temp_loop.run_until_complete(self.async_adapter.session_manager.remove_session())
                    finally:
                        temp_loop.close()
                except Exception as e:
                    print(f"Error in async cleanup: {e}")

Context Pool Manager
------------------

Manage multiple scenario contexts:

.. code-block:: python

    # features/scenario_context_pool_manager.py
    from uuid import UUID

    from archipy.helpers.metaclasses.singleton import Singleton
    from features.scenario_context import ScenarioContext

    class ScenarioContextPoolManager(metaclass=Singleton):
        """Manager for scenario-specific context objects."""

        def __init__(self):
            """Initialize the pool manager."""
            self.context_pool = {}

        def get_context(self, scenario_id: UUID) -> ScenarioContext:
            """Get or create a scenario context for the given ID."""
            if scenario_id not in self.context_pool:
                self.context_pool[scenario_id] = ScenarioContext(scenario_id)
            return self.context_pool[scenario_id]

        def cleanup_context(self, scenario_id: UUID) -> None:
            """Clean up a specific scenario context."""
            if scenario_id in self.context_pool:
                self.context_pool[scenario_id].cleanup()
                del self.context_pool[scenario_id]

        def cleanup_all(self) -> None:
            """Clean up all scenario contexts."""
            for scenario_id, context in list(self.context_pool.items()):
                context.cleanup()
                del self.context_pool[scenario_id]

Step Implementation
-----------------

Implementing steps with context management:

.. code-block:: python

    # features/steps/user_steps.py
    from behave import given, when, then
    from sqlalchemy import select

    from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import SqlAlchemyAdapter, AsyncSqlAlchemyAdapter
    from archipy.adapters.orm.sqlalchemy.sqlalchemy_mocks import SqlAlchemyMock, AsyncSqlAlchemyMock
    from features.test_helpers import get_current_scenario_context
    from features.test_entity import User

    @given("the application database is initialized")
    def step_given_database_initialized(context):
        # Get isolated context for this scenario
        scenario_context = get_current_scenario_context(context)

        # Create mock adapter for testing
        adapter = SqlAlchemyMock()
        scenario_context.adapter = adapter

        # Create tables
        User.__table__.create(adapter.session_manager.engine)

        # Store adapter in context
        scenario_context.store("adapter", adapter)

    @when('a new user "{name}" with email "{email}" is created')
    def step_when_create_user(context, name, email):
        scenario_context = get_current_scenario_context(context)
        adapter = scenario_context.get("adapter")

        # Create user with atomic transaction
        from archipy.helpers.utils.atomic_transaction import atomic_transaction

        with atomic_transaction(adapter.session_manager):
            user = User(name=name, email=email)
            adapter.create(user)
            scenario_context.store("user", user)

    @then("the user should exist in the database")
    def step_then_user_exists(context):
        scenario_context = get_current_scenario_context(context)
        adapter = scenario_context.get("adapter")
        user = scenario_context.get("user")

        # Query for user
        stored_user = adapter.get_by_uuid(User, user.test_uuid)
        assert stored_user is not None

    @given('a user with email "{email}" exists')
    def step_given_user_exists(context, email):
        scenario_context = get_current_scenario_context(context)

        # Create async mock adapter
        adapter = AsyncSqlAlchemyMock()
        scenario_context.async_adapter = adapter

        # Create tables
        import asyncio

        async def setup_async_db():
            await User.__table__.create(adapter.session_manager.engine)

            # Create a test user
            user = User(name="Test User", email=email)
            await adapter.create(user)
            return user

        # Run async setup
        user = asyncio.run(setup_async_db())
        scenario_context.store("async_user", user)
        scenario_context.store("async_adapter", adapter)

    @when("I retrieve the user by email asynchronously")
    def step_when_retrieve_user_async(context):
        import asyncio
        scenario_context = get_current_scenario_context(context)
        adapter = scenario_context.get("async_adapter")
        user = scenario_context.get("async_user")

        async def retrieve_user():
            from archipy.helpers.utils.atomic_transaction import async_atomic_transaction

            async with async_atomic_transaction(adapter.session_manager):
                query = select(User).where(User.email == user.email)
                users, total = await adapter.execute_search_query(User, query)
                return users[0] if users else None

        # Run async retrieval
        retrieved_user = asyncio.run(retrieve_user())
        scenario_context.store("retrieved_user", retrieved_user)

    @then("the user details should be retrieved successfully")
    def step_then_user_details_match(context):
        scenario_context = get_current_scenario_context(context)
        original_user = scenario_context.get("async_user")
        retrieved_user = scenario_context.get("retrieved_user")

        assert retrieved_user is not None
        assert retrieved_user.test_uuid == original_user.test_uuid
        assert retrieved_user.email == original_user.email

Helper Utilities
--------------

ArchiPy provides test helpers for BDD scenarios:

.. code-block:: python

    # features/test_helpers.py
    from behave.runner import Context

    def get_current_scenario_context(context: Context):
        """Get the current scenario context from the context pool."""
        scenario_id = context.scenario._id
        return context.scenario_context_pool.get_context(scenario_id)

    class SafeAsyncContextManager:
        """A safe async context manager for use in both sync and async code."""

        def __init__(self, context_manager_factory):
            self.context_manager_factory = context_manager_factory

        async def __aenter__(self):
            self.context_manager = self.context_manager_factory()
            return await self.context_manager.__aenter__()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return await self.context_manager.__aexit__(exc_type, exc_val, exc_tb)

Running BDD Tests
---------------

Execute tests with the behave command:

.. code-block:: bash

    # Run all tests
    behave

    # Run specific feature
    behave features/user_management.feature

    # Run async scenarios
    behave --tags=@async

    # Generate HTML report
    behave -f html -o reports/behave-report.html
