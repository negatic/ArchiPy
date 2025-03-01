.. _architecture:

Architecture
===========

Overview
--------

ArchiPy follows a hexagonal (Ports and Adapters) architecture, promoting separation of concerns and testability.

.. image:: https://img.shields.io/badge/Architecture-Hexagonal-brightgreen
   :alt: Hexagonal Architecture

Key Components
--------------

Adapters
~~~~~~~~

Adapters are implementations of ports that connect the application to external systems:

- **ORM Adapters**: Connect to databases (SQLAlchemy, etc.)
- **Redis Adapters**: Connect to Redis for caching
- **Email Adapters**: Connect to email services
- **gRPC Adapters**: Connect to gRPC services

Ports
~~~~

Ports define interfaces that adapters must implement:

- **SessionManagerPort**: Interface for database session management
- **SqlAlchemyPort**: Interface for SQLAlchemy operations
- **RedisPort**: Interface for Redis operations
- **EmailPort**: Interface for email operations

Models
~~~~~~

Standardize data:

- **Entities**: Database models (e.g., SQLAlchemy models)
- **DTOs**: Data Transfer Objects (using Pydantic)
- **Types**: Enums and custom types
- **Errors**: Custom error classes

Helpers
~~~~~~~

Enhance productivity:

- **Utils**: Various utility functions
- **Decorators**: Various decorators for methods and classes
- **Interceptors**: Middleware for gRPC, FastAPI, etc.
- **Metaclasses**: Special classes like Singleton

Configs
~~~~~~~

Standardize setup:

- **BaseConfig**: `base_config.py`
- **Templates**: `config_template.py`

Hexagonal Design
----------------

- **Core**: Business logic (models, helpers).
- **Ports**: Interfaces for external interaction.
- **Adapters**: Implementations for external systems.

Benefits:
1. Testability with mocks.
2. Flexibility in swapping adapters.
3. Clear boundaries.

Dependency Injection
--------------------

Example:

.. code-block:: python

   from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import SqlAlchemyAdapter
   service_repository = MyServiceRepository(sqlalchemy_adapter=SqlAlchemyAdapter())  # Inject adapter
   service = MyService(repository=service_repository)
