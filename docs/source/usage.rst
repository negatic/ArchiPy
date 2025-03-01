.. _usage:

Usage
=====

Getting Started
--------------

After installing ArchiPy, import its components to leverage its structured architecture:

.. code-block:: python

   import archipy

Examples
--------

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

Standardize and inject configurations:

.. code-block:: python

   from archipy.configs.base_config import BaseConfig

   # Define a custom config
   class MyAppConfig(BaseConfig):
       database_url: str = "sqlite:///example.db"
       redis_host: str = "localhost"

   config = MyAppConfig()
   print(config.database_url)  # "sqlite:///example.db"

Adapters & Mocks
~~~~~~~~~~~~~~~~

Use adapters for external systems with mocks for testing:

.. code-block:: python

   from archipy.adapters.redis.redis_adapters import AsyncRedisAdapter
   from archipy.adapters.redis.redis_mocks import AsyncRedisMock

   # Production use
   redis = AsyncRedisAdapter()
   await redis.set("key", "value", ex=3600)
   print(await redis.get("key"))  # "value"

   # Testing with mock
   mock_redis = AsyncRedisMock()
   await mock_redis.set("key", "test")
   print(await mock_redis.get("key"))  # "test"

Entities & DTOs
~~~~~~~~~~~~~~~

Standardize data models:

.. code-block:: python

   from sqlalchemy import Column, Integer, String
   from archipy.models.entities.sqlalchemy.base_entities import BaseEntity
   from archipy.models.dtos.base_dtos import BaseDTO

   # Entity
   class User(BaseEntity):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       name = Column(String(100))

   # DTO
   class UserDTO(BaseDTO):
       id: int
       name: str

   user = UserDTO(id=1, name="Alice")
   print(user.model_dump())  # {'id': 1, 'name': 'Alice'}

Helper Utilities
~~~~~~~~~~~~~~~~

Simplify tasks with utilities and decorators:

.. code-block:: python

   from archipy.helpers.utils.datetime_utils import get_utc_now
   from archipy.helpers.decorators.retry import retry

   # Utility
   now = get_utc_now()
   print(now)  # Current UTC time

   # Decorator
   @retry(max_attempts=3, delay=1)
   def risky_operation():
       # Simulated failure
       raise ValueError("Try again")

   try:
       risky_operation()
   except ValueError as e:
       print(f"Failed after retries: {e}")

BDD Testing
~~~~~~~~~~~

Validate features with `behave`:

.. code-block:: bash

   # Run BDD tests
   make behave

Example feature file (`features/app_utils.feature`):

.. code-block:: gherkin

   Feature: Application Utilities
     Scenario: Get UTC time
       When I get the current UTC time
       Then the result should be a valid datetime

Async Operations
~~~~~~~~~~~~~~~~

Support for asynchronous workflows:

.. code-block:: python

   import asyncio
   from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import AsyncSqlAlchemyAdapter

   async def fetch_users():
       adapter = AsyncSqlAlchemyAdapter(session_manager, User)
       users = await adapter.execute_search_query(User, pagination=None, sort_info=None)
       return users

   users, total = asyncio.run(fetch_users())
   print(users)  # List of User entities

Available Commands
------------------

Run ``make help`` for all commands. Common ones:

- **Format Code**: ``make format``
- **Lint Code**: ``make lint``
- **Run BDD Tests**: ``make behave``
- **Build Project**: ``make build``
- **Clean Artifacts**: ``make clean``
