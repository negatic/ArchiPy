.. _usage:

Usage
=====

Getting Started
--------------

After installing ArchiPy, you can import it in your Python code:

.. code-block:: python

   import archipy

Basic Examples
-------------

Configuration
~~~~~~~~~~~~

ArchiPy provides configuration templates for various services:

.. code-block:: python

   from archipy.configs.config_template import SqlAlchemyConfig, RedisConfig

   # Set up database configuration
   db_config = SqlAlchemyConfig(
       url="postgresql://user:password@localhost:5432/db_name",
       pool_size=5,
       max_overflow=10
   )

   # Set up Redis configuration
   redis_config = RedisConfig(
       host="localhost",
       port=6379,
       db=0
   )

Using SQLAlchemy Adapters
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import SqlAlchemyAdapter
   from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter

   # Create a session manager
   session_manager = SessionManagerAdapter(db_config)

   # Create a SQLAlchemy adapter
   adapter = SqlAlchemyAdapter(session_manager, YourEntity)

   # Use the adapter
   results = adapter.find_all()

Working with Entities
~~~~~~~~~~~~~~~~~~~

ArchiPy provides base entity classes for your database models:

.. code-block:: python

   from sqlalchemy import Column, Integer, String
   from archipy.models.entities.sqlalchemy.base_entities import BaseEntity

   class User(BaseEntity):
       __tablename__ = "users"

       id = Column(Integer, primary_key=True)
       name = Column(String(100))
       email = Column(String(100))

Using DTOs (Data Transfer Objects)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pydantic import Field
   from archipy.models.dtos.base_dtos import BaseDTO

   class UserDTO(BaseDTO):
       id: int
       name: str
       email: str
       age: int = Field(gt=0)

Making Async Requests
~~~~~~~~~~~~~~~~~~~

ArchiPy supports async operations for database and Redis:

.. code-block:: python

   import asyncio
   from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import AsyncSqlAlchemyAdapter

   async def fetch_data():
       adapter = AsyncSqlAlchemyAdapter(async_session_manager, YourEntity)
       results = await adapter.find_all()
       return results

   # Run the async function
   asyncio.run(fetch_data())

Error Handling
~~~~~~~~~~~~

ArchiPy provides a comprehensive set of custom errors:

.. code-block:: python

   from archipy.models.errors.custom_errors import NotFoundError, InvalidArgumentError

   try:
       # Your code here
       if not valid_input:
           raise InvalidArgumentError("Invalid input provided")
   except NotFoundError as e:
       # Handle not found error
       print(f"Resource not found: {str(e)}")
   except InvalidArgumentError as e:
       # Handle invalid argument error
       print(f"Invalid argument: {str(e)}")

Available Commands
----------------

Run ``make help`` to see all available commands:

.. code-block:: bash

   make help

Common Commands
~~~~~~~~~~~~~

Format Code:

.. code-block:: bash

   make format

Run Linters:

.. code-block:: bash

   make lint

Run Tests:

.. code-block:: bash

   make behave

Build the Project:

.. code-block:: bash

   make build

Clean Build Artifacts:

.. code-block:: bash

   make clean
