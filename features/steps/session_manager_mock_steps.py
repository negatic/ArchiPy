import asyncio
import uuid
from datetime import datetime

from behave import given, then, when
from features.test_entity import TestEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from archipy.adapters.orm.sqlalchemy.session_manager_mocks import AsyncSessionManagerMock, SessionManagerMock
from archipy.adapters.orm.sqlalchemy.sqlalchemy_mocks import AsyncSqlAlchemyMock, SqlAlchemyMock
from archipy.configs.config_template import SqlAlchemyConfig
from archipy.models.entities import BaseEntity


@given("a SessionManagerMock instance")
def step_given_session_manager_mock(context):
    context.session_manager = SessionManagerMock()


@given("an AsyncSessionManagerMock instance")
def step_given_async_session_manager_mock(context):
    context.session_manager = AsyncSessionManagerMock()


@when("another SessionManagerMock instance is created")
def step_when_another_session_manager_mock_is_created(context):
    context.new_session_manager = SessionManagerMock()


@when("another AsyncSessionManagerMock instance is created")
def step_when_another_async_session_manager_mock_is_created(context):
    context.new_session_manager = AsyncSessionManagerMock()


@then("both instances should be the same")
def step_then_instances_should_be_singleton(context):
    assert context.session_manager is context.new_session_manager


@when("a session is acquired")
def step_when_session_is_acquired(context):
    context.session = context.session_manager.get_session()


@then("the session should not be None")
def step_then_session_should_not_be_none(context):
    assert isinstance(context.session, Session), "Session is not of type SQLAlchemy Session"


@when("the session is removed")
def step_when_session_is_removed(context):
    context.session_manager.remove_session()


@then("acquiring a new session should not be the same as the previous one")
def step_then_new_session_should_not_be_same(context):
    new_session = context.session_manager.get_session()
    assert new_session is not context.session, "New session instance was not created"


@when("an async session is acquired")
def step_when_async_session_is_acquired(context):
    """Ensures async session is retrieved inside an event loop."""

    async def acquire_session():
        context.session = context.session_manager.get_session()

    asyncio.run(acquire_session())


@then("the async session should not be None")
def step_then_async_session_should_not_be_none(context):
    assert isinstance(context.session, AsyncSession), "Async session is not of type SQLAlchemy AsyncSession"


@when("the async session is removed")
def step_when_async_session_is_removed(context):
    """Ensures async session is properly awaited in Behave."""

    async def remove_async_session():
        await context.session_manager.remove_session()

    asyncio.run(remove_async_session())


@then("acquiring a new async session should not be the same as the previous one")
def step_then_new_async_session_should_not_be_same(context):
    async def get_async_session():
        new_async_session = context.session_manager.get_session()
        assert new_async_session is not context.session, "New async session instance was not created"

    asyncio.run(get_async_session())


@when("an SQLite engine is created")
def step_when_sqlite_engine_is_created(context):
    context.engine = context.session_manager._create_engine(
        SqlAlchemyConfig(
            DRIVER_NAME="sqlite",
            DATABASE=":memory:",
            ISOLATION_LEVEL=None,
            PORT=None,
        ),
    )


@then("the engine connection should be successful")
def step_then_sqlite_connection_should_work(context):
    assert context.engine is not None, "SQLite engine was not created"
    connection = context.engine.connect()
    assert connection is not None, "Unable to establish a connection"
    connection.close()


@when("an Async SQLite engine is created")
def step_when_async_sqlite_engine_is_created(context):
    context.async_engine = context.session_manager._create_async_engine(
        SqlAlchemyConfig(
            DRIVER_NAME="sqlite+aiosqlite",
            DATABASE=":memory:",
            ISOLATION_LEVEL=None,
            PORT=None,
        ),
    )


@then("the async engine connection should be successful")
def step_then_async_sqlite_connection_should_work(context):
    assert context.async_engine is not None, "Async SQLite engine was not created"

    async def async_test():
        connection = await context.async_engine.connect()
        assert connection is not None, "Unable to establish an async connection"
        await connection.close()

    asyncio.run(async_test())


@given("a adapter is acquired")
def step_given_sqlite_test_db(context):
    """Setup SQLite in-memory database"""
    context.adapter = SqlAlchemyMock()


@when("an SQLite test database is set up")
def step_given_sqlite_test_db(context):
    """Setup SQLite in-memory database"""
    BaseEntity.metadata.drop_all(context.adapter.session_manager.engine)
    BaseEntity.metadata.create_all(context.adapter.session_manager.engine)


@given("a async adapter is acquired")
def step_given_sqlite_test_db(context):
    """Setup SQLite in-memory database"""

    async def initialize_adapter():
        context.adapter = AsyncSqlAlchemyMock()
        context.session = context.adapter.session_manager.get_session()

    asyncio.run(initialize_adapter())


@when("an async SQLite test database is set up")
def step_given_async_sqlite_test_db(context):
    """Setup SQLite async database"""

    async def initialize_database():
        async with context.adapter.session_manager.engine.begin() as conn:
            await conn.run_sync(BaseEntity.metadata.create_all)
            await conn.run_sync(BaseEntity.metadata.create_all)

    asyncio.run(initialize_database())


@when("a new entity is created and saved")
def step_when_entity_is_created(context):
    context.test_entity = TestEntity(test_uuid=uuid.uuid4(), created_at=datetime.now())
    context.adapter.create(context.test_entity)
    context.adapter.get_session().commit()


@then("the entity should be retrievable")
def step_then_entity_should_be_retrieved(context):
    session = context.adapter.get_session()
    retrieved_entity = session.get(TestEntity, context.test_entity.pk_uuid)
    assert retrieved_entity is not None, "Entity not found in database"


@when("the entity is deleted")
def step_when_entity_is_deleted(context):
    session = context.adapter.get_session()
    session.delete(context.test_entity)
    session.commit()


@then("retrieving it should return None")
def step_then_entity_should_not_be_found(context):
    session = context.adapter.get_session()
    deleted_entity = session.get(TestEntity, context.test_entity.pk_uuid)
    assert deleted_entity is None, "Entity was not deleted from the database"


@when("an async new entity is created and saved")
def step_when_async_entity_is_created(context):
    async def create_entity():
        context.test_entity = TestEntity(test_uuid=uuid.uuid4(), created_at=datetime.now())
        await context.adapter.create(context.test_entity)
        await context.session.commit()

    asyncio.run(create_entity())


@then("the async entity should be retrievable")
def step_then_async_entity_should_be_retrieved(context):
    async def retrieve_entity():
        session = context.adapter.get_session()
        retrieved_entity = session.get(TestEntity, context.test_entity.pk_uuid)
        assert retrieved_entity is not None, "Entity not found in database"

    asyncio.run(retrieve_entity())


@when("the async entity is deleted")
def step_when_async_entity_is_deleted(context):
    async def delete_entity():
        await context.adapter.delete(context.test_entity)
        await context.session.commit()

    asyncio.run(delete_entity())


@then("async retrieving it should return None")
def step_then_async_entity_should_not_be_found(context):
    async def retrieve_deleted():
        session = context.adapter.get_session()
        deleted_entity = await session.get(TestEntity, context.test_entity.pk_uuid)
        assert deleted_entity is None, "Entity was not deleted from the database"

    asyncio.run(retrieve_deleted())
