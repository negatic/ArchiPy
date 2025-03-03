.. _api_adapters:

Adapters
========

.. admonition:: Overview
   :class: note

   The adapters module provides standardized interfaces to external systems like databases,
   cache services, and email providers. Each adapter type includes both production implementations
   and testing mocks to support isolated testing.

   **See Examples**: :ref:`examples_adapters`

Module Structure
---------------

.. figure:: ../assets/adapters_structure.png
   :alt: Adapters Module Structure
   :align: center
   :width: 70%

   Organization of the adapters module

ORM Adapters
-----------

Database adapters built on SQLAlchemy:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: SqlAlchemyAdapter
        :link: #sqlalchemy-adapter
        :class-card: sd-rounded-3

        Synchronous adapter for SQL database operations.

    .. grid-item-card:: AsyncSqlAlchemyAdapter
        :link: #async-sqlalchemy-adapter
        :class-card: sd-rounded-3

        Asynchronous adapter for SQL database operations.

    .. grid-item-card:: SessionManagerAdapter
        :link: #session-manager
        :class-card: sd-rounded-3

        Manages database sessions and connections.

    .. grid-item-card:: Mocks
        :link: #orm-mocks
        :class-card: sd-rounded-3

        Testing mocks for database operations.

Redis Adapters
-------------

Cache and message broker adapters:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: RedisAdapter
        :link: #redis-adapter
        :class-card: sd-rounded-3

        Synchronous adapter for Redis operations.

    .. grid-item-card:: AsyncRedisAdapter
        :link: #async-redis-adapter
        :class-card: sd-rounded-3

        Asynchronous adapter for Redis operations.

    .. grid-item-card:: RedisMock
        :link: #redis-mocks
        :class-card: sd-rounded-3

        Testing mock for Redis operations.

Email Adapters
-------------

Email sending adapters:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: EmailAdapter
        :link: #email-adapter
        :class-card: sd-rounded-3

        Adapter for sending emails via SMTP.

    .. grid-item-card:: EmailMock
        :link: #email-mock
        :class-card: sd-rounded-3

        Testing mock for email operations.

Key Classes & Interfaces
-----------------------

.. _sqlalchemy-adapter:

SqlAlchemyAdapter
~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.SqlAlchemyAdapter
   :members:
   :noindex:

Example:

.. code-block:: python

    from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import SqlAlchemyAdapter
    from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter

    # Create a session manager
    session_manager = SessionManagerAdapter()

    # Create an adapter
    db = SqlAlchemyAdapter(session_manager)

    # Use the adapter
    user = User(name="John Doe")
    db.create(user)

    # Query data
    from sqlalchemy import select
    query = select(User).where(User.name == "John Doe")
    users, total = db.execute_search_query(User, query)

.. _async-sqlalchemy-adapter:

AsyncSqlAlchemyAdapter
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.AsyncSqlAlchemyAdapter
   :members:
   :noindex:

Example:

.. code-block:: python

    import asyncio
    from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import AsyncSqlAlchemyAdapter
    from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter

    async def create_user():
        # Create async session manager and adapter
        session_manager = AsyncSessionManagerAdapter()
        db = AsyncSqlAlchemyAdapter(session_manager)

        # Create user
        user = User(name="John Doe")
        await db.create(user)

        # Query data
        from sqlalchemy import select
        query = select(User).where(User.name == "John Doe")
        users, total = await db.execute_search_query(User, query)
        return users

    # Run the async function
    users = asyncio.run(create_user())

.. _session-manager:

SessionManagerAdapter
~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.session_manager_adapters.SessionManagerAdapter
   :members:
   :noindex:

.. autoclass:: archipy.adapters.orm.sqlalchemy.session_manager_adapters.AsyncSessionManagerAdapter
   :members:
   :noindex:

.. _orm-mocks:

ORM Mocks
~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_mocks.SqlAlchemyMock
   :members:
   :noindex:

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_mocks.AsyncSqlAlchemyMock
   :members:
   :noindex:

.. autoclass:: archipy.adapters.orm.sqlalchemy.session_manager_mocks.SessionManagerMock
   :members:
   :noindex:

.. autoclass:: archipy.adapters.orm.sqlalchemy.session_manager_mocks.AsyncSessionManagerMock
   :members:
   :noindex:

.. _redis-adapter:

RedisAdapter
~~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_adapters.RedisAdapter
   :members:
   :noindex:

.. _async-redis-adapter:

AsyncRedisAdapter
~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_adapters.AsyncRedisAdapter
   :members:
   :noindex:

.. _redis-mocks:

Redis Mocks
~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_mocks.RedisMock
   :members:
   :noindex:

.. autoclass:: archipy.adapters.redis.redis_mocks.AsyncRedisMock
   :members:
   :noindex:

.. _email-adapter:

EmailAdapter
~~~~~~~~~~~

.. autoclass:: archipy.adapters.email.email_adapter.EmailAdapter
   :members:
   :noindex:

.. _email-mock:

EmailMock
~~~~~~~~

.. autoclass:: archipy.adapters.email.email_mocks.EmailMock
   :members:
   :noindex:

Design Patterns
--------------

Adapters in ArchiPy follow these patterns:

1. **Ports & Adapters Pattern**: Interfaces (ports) define the contract, and implementations (adapters) provide concrete functionality

2. **Dependency Injection**: Adapters accept dependencies rather than creating them internally

3. **Testing Isolation**: Each adapter has a corresponding mock for unit testing without external dependencies

4. **Consistent Interfaces**: Common patterns across different adapter types

5. **Configuration-Driven**: Adapters use settings from global configuration
