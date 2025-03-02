.. _examples_adapters_orm:

ORM Adapters
==========

Database operations using SQLAlchemy adapters.

Configuration
------------

First, configure your database settings:

.. code-block:: python

    from archipy.configs.base_config import BaseConfig

    class AppConfig(BaseConfig):
        SQLALCHEMY = {
            "DRIVER_NAME": "postgresql",
            "USERNAME": "postgres",
            "PASSWORD": "password",
            "HOST": "localhost",
            "PORT": 5432,
            "DATABASE": "myapp",
            "POOL_SIZE": 10
        }

    # Set global configuration
    config = AppConfig()
    BaseConfig.set_global(config)

Defining Models
-------------

Define your database models:

.. code-block:: python

    from uuid import uuid4
    from sqlalchemy import Column, String, ForeignKey
    from sqlalchemy.orm import relationship
    from archipy.models.entities import BaseEntity

    class User(BaseEntity):
        __tablename__ = "users"

        name = Column(String(100))
        email = Column(String(100), unique=True)

        # Relationships
        posts = relationship("Post", back_populates="author")

    class Post(BaseEntity):
        __tablename__ = "posts"

        title = Column(String(255))
        content = Column(String(1000))

        # Foreign keys
        author_id = Column(String(36), ForeignKey("users.test_uuid"))

        # Relationships
        author = relationship("User", back_populates="posts")

Synchronous Operations
-------------------

Examples of synchronous database operations:

.. code-block:: python

    from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter
    from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import SqlAlchemyAdapter
    from sqlalchemy import select

    # Create session manager and adapter
    session_manager = SessionManagerAdapter()
    adapter = SqlAlchemyAdapter(session_manager)

    # Create a user
    def create_user(name, email):
        user = User(test_uuid=uuid4(), name=name, email=email)
        return adapter.create(user)

    # Query users
    def find_users_by_name(name):
        query = select(User).where(User.name == name)
        users, total = adapter.execute_search_query(User, query)
        return users

    # Update a user
    def update_user_email(user_id, new_email):
        user = adapter.get_by_uuid(User, user_id)
        if user:
            user.email = new_email
            return adapter.update(user)
        return None

    # Delete a user
    def delete_user(user_id):
        user = adapter.get_by_uuid(User, user_id)
        if user:
            adapter.delete(user)
            return True
        return False

Asynchronous Operations
--------------------

Examples of asynchronous database operations:

.. code-block:: python

    import asyncio
    from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter
    from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import AsyncSqlAlchemyAdapter

    # Create async session manager and adapter
    async_session_manager = AsyncSessionManagerAdapter()
    async_adapter = AsyncSqlAlchemyAdapter(async_session_manager)

    # Create a user asynchronously
    async def create_user_async(name, email):
        user = User(test_uuid=uuid4(), name=name, email=email)
        return await async_adapter.create(user)

    # Query users asynchronously
    async def find_users_by_name_async(name):
        query = select(User).where(User.name == name)
        users, total = await async_adapter.execute_search_query(User, query)
        return users

    # Usage with asyncio
    async def main():
        # Create a user
        user = await create_user_async("John Doe", "john@example.com")

        # Find users
        users = await find_users_by_name_async("John Doe")
        print(f"Found {len(users)} users")

    # Run the async function
    asyncio.run(main())

Transactions
-----------

Using transactions to ensure consistency:

.. code-block:: python

    from archipy.helpers.utils.atomic_transaction import atomic_transaction, async_atomic_transaction

    # Synchronous transaction
    def transfer_points(from_user_id, to_user_id, amount):
        with atomic_transaction(adapter.session_manager):
            from_user = adapter.get_by_uuid(User, from_user_id)
            to_user = adapter.get_by_uuid(User, to_user_id)

            # Perform operations atomically
            from_user.points -= amount
            to_user.points += amount

            adapter.update(from_user)
            adapter.update(to_user)

    # Asynchronous transaction
    async def transfer_points_async(from_user_id, to_user_id, amount):
        async with async_atomic_transaction(async_adapter.session_manager):
            from_user = await async_adapter.get_by_uuid(User, from_user_id)
            to_user = await async_adapter.get_by_uuid(User, to_user_id)

            # Perform operations atomically
            from_user.points -= amount
            to_user.points += amount

            await async_adapter.update(from_user)
            await async_adapter.update(to_user)
