# Solving Database Isolation Level Issues in Multi-Pod Environments: A Practical Approach with Archipy

## Related Articles

Before diving into this article, I recommend reading my previous posts that provide essential context:

- [Understanding Database Isolation Levels from My Perspective](https://medium.com/@hosseinnejati/understanding-database-isolation-levels-from-my-perspective-27f261eeb976)
- [Why Lazy Loading in Databases Feels Useful but Scary to Me](https://medium.com/@hosseinnejati/why-lazy-loading-in-databases-feels-useful-but-scary-to-me-60353d98580b)
- [Understanding the Unit of Work Pattern with Archipy](https://medium.com/@hosseinnejati/understanding-the-unit-of-work-pattern-with-archipy-4d9ac6fef7a4)

---

## Introduction

Database isolation levels are fundamental to maintaining data consistency in concurrent environments, but they can introduce unexpected challenges when working with lazy loading in distributed systems. In this article, I will share a real-world problem I encountered when using SQLAlchemy with SERIALIZABLE and REPEATABLE READ isolation levels in a multi-pod Kubernetes environment, and demonstrate how I solved it with a custom atomic decorator in my Archipy framework.

## The Problem: Lazy Loading Returns Stale Data

### The Scenario

In my microservices architecture running on Kubernetes, I had multiple pods accessing the same PostgreSQL database. I was using SQLAlchemy with higher isolation levels (SERIALIZABLE or REPEATABLE READ) to ensure data consistency. However, I discovered a critical issue: lazy loading was returning stale data when one pod updated records while another pod was reading them.

### Root Cause Analysis

The problem stems from how SQLAlchemy's session management interacts with database isolation levels:

1. **Session Persistence**: SQLAlchemy sessions can persist across multiple operations
2. **Isolation Level Behavior**: Higher isolation levels (REPEATABLE READ, SERIALIZABLE) maintain a consistent snapshot of data throughout a transaction
3. **Lazy Loading Timing**: When lazy loading occurs, it uses the same session that might have been created before other pods made updates
4. **Cross-Pod Updates**: Updates from other pods become invisible to existing sessions due to isolation level constraints

### Configuration Context

In my Archipy framework, I configure isolation levels through the SQLAlchemyConfig:

    class SQLAlchemyConfig(BaseModel):
        """Configuration settings for SQLAlchemy ORM.

        Controls database connection parameters, pooling behavior, and query execution settings.
        """

        ISOLATION_LEVEL: str | None = Field(
            default="REPEATABLE READ",
            description="Transaction isolation level"
        )
        # ... other configuration fields

This configuration is used when creating the SQLAlchemy engine:

    def _create_engine(self, configs: SQLAlchemyConfig) -> Engine:
        """Create a SQLAlchemy engine with common configuration."""
        try:
            url = self._create_url(configs)
            return create_engine(
                url,
                isolation_level=configs.ISOLATION_LEVEL,
                echo=configs.ECHO,
                echo_pool=configs.ECHO_POOL,
                # ... other engine parameters
            )
        except SQLAlchemyError as e:
            # Error handling logic
            pass

## The Solution: Atomic Decorator with Session Cleanup

### Design Requirements

I needed a solution that would:

1. Ensure transactional integrity for unit of work operations
2. Clean up sessions properly to prevent stale data issues
3. Handle both synchronous and asynchronous operations
4. Support multiple database types (PostgreSQL, SQLite, StarRocks)
5. Provide proper error handling with database-specific exceptions

### Implementation Overview

I created a comprehensive atomic decorator system in `archipy/helpers/decorators/sqlalchemy_atomic.py`:

    def sqlalchemy_atomic_decorator(
        db_type: str,
        is_async: bool = False,
        function: Callable[..., Any] | None = None,
    ) -> Callable[..., Any] | partial[Callable[..., Any]]:
        """Factory for creating SQLAlchemy atomic transaction decorators.

        This decorator ensures that a function runs within a database transaction for the specified
        database type. If the function succeeds, the transaction is committed; otherwise, it is rolled back.
        Supports both synchronous and asynchronous functions.

        Args:
            db_type (str): The database type ("postgres", "sqlite", or "starrocks").
            is_async (bool): Whether the function is asynchronous. Defaults to False.
            function (Callable | None): The function to wrap. If None, returns a partial function.

        Returns:
            Callable | partial: The wrapped function or a partial function for later use.
        """

### Key Implementation Features

#### 1. Automatic Session Management

The decorator handles the complete session lifecycle:

    def sync_wrapper(*args: Any, **kwargs: Any) -> R:
        """Synchronous wrapper for managing database transactions."""
        registry = get_registry()
        session_manager: SessionManagerPort = registry.get_sync_manager()
        session = session_manager.get_session()
        is_nested = session.info.get(atomic_flag, False)
        if not is_nested:
            session.info[atomic_flag] = True

        try:
            if session.in_transaction():
                result = func(*args, **kwargs)
                if not is_nested:
                    session.commit()
                return result
            with session.begin():
                return func(*args, **kwargs)
        except Exception as exception:
            session.rollback()
            _handle_db_exception(exception, db_type, func.__name__)
        finally:
            if not session.in_transaction():
                session.close()
                session_manager.remove_session()

        return sync_wrapper

#### 2. Critical Session Cleanup

The solution to the stale data problem lies in the finally block:

    finally:
        if not session.in_transaction():
            session.close()
            session_manager.remove_session()

This ensures:
- Sessions are properly closed after each atomic operation
- The session registry is cleaned up
- Subsequent operations get fresh sessions with current data

#### 3. Database-Specific Error Handling

The decorator includes sophisticated error handling for different database scenarios:

    def _handle_db_exception(exception: Exception, db_type: str, func_name: str) -> None:
        """Handle database exceptions and raise appropriate errors."""
        logging.debug(f"Exception in {db_type} atomic block (func: {func_name}): {exception}")

        if isinstance(exception, OperationalError):
            if hasattr(exception, "orig") and exception.orig:
                sqlstate = getattr(exception.orig, "pgcode", None)
                if sqlstate == "40001":  # Serialization failure
                    raise DatabaseSerializationError(database=db_type) from exception
                if sqlstate == "40P01":  # Deadlock detected
                    raise DatabaseDeadlockError(database=db_type) from exception

            # SQLite-specific errors
            if "database is locked" in str(exception):
                raise DatabaseDeadlockError(database=db_type) from exception

            # Generic operational errors
            raise DatabaseConnectionError(database=db_type) from exception

#### 4. Support for Nested Transactions

The decorator intelligently handles nested atomic blocks:

    is_nested = session.info.get(atomic_flag, False)
    if not is_nested:
        session.info[atomic_flag] = True

#### 5. Asynchronous Support

The decorator also provides full async support:

    async def async_wrapper(*args: Any, **kwargs: Any) -> R:
        """Async wrapper for managing database transactions."""
        registry = get_registry()
        session_manager: AsyncSessionManagerPort = registry.get_async_manager()
        session = session_manager.get_session()
        is_nested = session.info.get(atomic_flag, False)
        if not is_nested:
            session.info[atomic_flag] = True

        try:
            if session.in_transaction():
                result = await func(*args, **kwargs)
                if not is_nested:
                    await session.commit()
                return result
            async with session.begin():
                return await func(*args, **kwargs)
        except Exception as exception:
            await session.rollback()
            _handle_db_exception(exception, db_type, func.__name__)
        finally:
            if not session.in_transaction():
                await session.close()
                await session_manager.remove_session()

    return async_wrapper

## Usage Examples

### Basic Synchronous Usage

    from archipy.helpers.decorators.sqlalchemy_atomic import postgres_sqlalchemy_atomic_decorator

    @postgres_sqlalchemy_atomic_decorator
    def update_user_profile(user_id: UUID, profile_data: dict) -> User:
        """Update user profile in an atomic transaction."""
        # Database operations here
        # Session will be automatically cleaned up
        adapter = get_user_adapter()
        user = adapter.get_by_uuid(User, user_id)
        user.update_profile(profile_data)
        return adapter.update(user)

### Asynchronous Operations

    from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

    @async_postgres_sqlalchemy_atomic_decorator
    async def process_payment(payment_id: UUID) -> PaymentResult:
        """Process payment asynchronously in an atomic transaction."""
        adapter = get_payment_adapter()
        payment = await adapter.get_by_uuid(Payment, payment_id)
        result = await payment_service.process(payment)
        await adapter.update(payment)
        return result

### Multi-Database Support

    # For SQLite
    from archipy.helpers.decorators.sqlalchemy_atomic import sqlite_sqlalchemy_atomic_decorator

    @sqlite_sqlalchemy_atomic_decorator
    def sqlite_operation():
        # SQLite-specific operations
        pass

    # For StarRocks
    from archipy.helpers.decorators.sqlalchemy_atomic import starrocks_sqlalchemy_atomic_decorator

    @starrocks_sqlalchemy_atomic_decorator
    def starrocks_operation():
        # StarRocks-specific operations
        pass

## Testing and Validation

I implemented comprehensive BDD tests using Behave to ensure the decorator works correctly across different scenarios:

    @when("operations are performed across multiple atomic blocks")
    def step_when_operations_across_multiple_atomics(context):
        """Test session consistency across multiple atomic blocks."""
        logger = getattr(context, "logger", logging.getLogger("behave.steps"))
        scenario_context = get_current_scenario_context(context)

        # Generate UUIDs for entities
        entity_uuids = [uuid.uuid4() for _ in range(3)]

        @sqlite_sqlalchemy_atomic_decorator
        def create_initial_entities():
            logger.info("Creating initial entities in first atomic block")
            entities = []
            for i, uuid_val in enumerate(entity_uuids):
                entity = TestEntityFactory.create_test_entity(
                    test_uuid=uuid_val,
                    description=f"Initial Entity {i + 1}"
                )
                adapter = get_adapter(context)
                adapter.create(entity)
                entities.append(entity)
            return entities

        @sqlite_sqlalchemy_atomic_decorator
        def update_entities():
            logger.info("Updating entities in second atomic block")
            adapter = get_adapter(context)
            session = adapter.get_session()

            for i, uuid_val in enumerate(entity_uuids):
                db_entity = session.get(TestEntity, uuid_val)
                db_entity.description = f"Updated Entity {i + 1}"
                db_entity.updated_at = datetime.now()
            return True

        @sqlite_sqlalchemy_atomic_decorator
        def query_entities():
            logger.info("Querying entities in third atomic block")
            adapter = get_adapter(context)
            session = adapter.get_session()

            results = []
            for i, uuid_val in enumerate(entity_uuids):
                db_entity = session.get(TestEntity, uuid_val)
                results.append({
                    "uuid": uuid_val,
                    "description": db_entity.description,
                    "updated_at": db_entity.updated_at
                })
            scenario_context.store("query_results", results)
            return results

        # Execute operations
        create_initial_entities()
        update_entities()
        query_entities()

## Results and Impact

### Before Implementation

- **Stale Data Issues**: Lazy loading returned outdated information across pods
- **Inconsistent Application State**: Different pods operated on different data snapshots
- **Difficult Debugging**: Issues were intermittent and environment-dependent
- **Unreliable Isolation Levels**: Higher isolation levels caused more problems than they solved

### After Implementation

- **Consistent Fresh Data**: Each atomic operation receives a clean session with current data
- **Predictable Cross-Pod Behavior**: All pods see the same current state of the database
- **Reliable Isolation Levels**: Isolation levels work as intended without side effects
- **Improved Error Handling**: Clear, specific exceptions for different failure scenarios
- **Better Debugging**: Comprehensive logging and predictable behavior patterns

## Best Practices and Recommendations

### 1. Always Use Atomic Decorators for Unit of Work Operations

    @postgres_sqlalchemy_atomic_decorator
    def complete_order_process(order_id: UUID) -> Order:
        """Complete entire order process as one unit of work."""
        # All related operations within one atomic block
        # Automatic session cleanup prevents stale data issues
        order_adapter = get_order_adapter()
        payment_adapter = get_payment_adapter()
        inventory_adapter = get_inventory_adapter()

        order = order_adapter.get_by_uuid(Order, order_id)
        payment = payment_adapter.process_payment(order.payment_info)
        inventory_adapter.reserve_items(order.items)

        order.mark_as_completed()
        return order_adapter.update(order)

### 2. Configure Appropriate Isolation Levels

    # In your configuration
    POSTGRES_SQLALCHEMY = PostgresSQLAlchemyConfig(
        ISOLATION_LEVEL="REPEATABLE READ",  # Choose based on your consistency requirements
        POOL_SIZE=20,
        POOL_MAX_OVERFLOW=1,
        POOL_PRE_PING=True,
        # ... other settings
    )

### 3. Handle Serialization Failures Gracefully

    from archipy.models.errors import DatabaseSerializationError

    def robust_operation_with_retry(data: dict, max_retries: int = 3) -> Result:
        """Perform operation with automatic retry on serialization failures."""
        for attempt in range(max_retries):
            try:
                return perform_atomic_operation(data)
            except DatabaseSerializationError as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Serialization failure on attempt {attempt + 1}, retrying...")
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff

### 4. Monitor Session Lifecycle

The decorator provides comprehensive logging for debugging and monitoring:

    # Enable debug logging to monitor session behavior
    logging.getLogger("archipy.helpers.decorators.sqlalchemy_atomic").setLevel(logging.DEBUG)

### 5. Test Across Multiple Pods

Always test your atomic operations in a multi-pod environment to ensure session cleanup works correctly:

    # Example test scenario
    def test_cross_pod_consistency():
        """Test that updates from one pod are visible to other pods."""

        # Pod 1: Create and update entity
        @postgres_sqlalchemy_atomic_decorator
        def pod1_operation():
            entity = create_test_entity()
            entity.status = "updated_by_pod1"
            return update_entity(entity)

        # Pod 2: Read entity (should see pod1's update)
        @postgres_sqlalchemy_atomic_decorator
        def pod2_operation():
            entity = get_entity_by_id(entity_id)
            assert entity.status == "updated_by_pod1"
            return entity

        entity = pod1_operation()
        retrieved_entity = pod2_operation()
        assert retrieved_entity.status == entity.status

## Conclusion

Database isolation levels are powerful tools for maintaining data consistency, but they require careful session management in distributed environments. The atomic decorator pattern I implemented in Archipy effectively solves the lazy loading stale data problem by ensuring proper session cleanup after each unit of work.

This solution provides several key benefits:

- **Automatic transaction management** with proper commit/rollback handling
- **Comprehensive session cleanup** that prevents stale data issues
- **Support for multiple databases** and both synchronous and asynchronous operations
- **Sophisticated error handling** with database-specific exception types
- **Nested transaction support** for complex business operations
- **Extensive testing coverage** with BDD scenarios

By implementing this pattern, development teams can confidently use higher isolation levels in multi-pod environments without encountering lazy loading stale data issues. The decorator abstracts away the complexity of session management while providing the reliability and consistency required for production systems.

The complete implementation is available in the Archipy framework, and I encourage other developers to adapt this pattern to their own projects when dealing with similar isolation level challenges in distributed environments.

This approach has proven effective in production environments and continues to provide reliable database operations across multiple Kubernetes pods while maintaining the data consistency guarantees that higher isolation levels are designed to provide.
