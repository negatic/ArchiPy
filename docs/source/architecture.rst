.. _architecture:

Architecture
===========

Overview
--------

ArchiPy follows a clean, hexagonal architecture pattern that separates concerns and promotes testability. The architecture is designed around the following key components:

.. image:: https://img.shields.io/badge/Architecture-Hexagonal-brightgreen
   :alt: Hexagonal Architecture

Key Components
-------------

Adapters
~~~~~~~

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
~~~~~

Models represent data structures:

- **Entities**: Database models (e.g., SQLAlchemy models)
- **DTOs**: Data Transfer Objects (using Pydantic)
- **Types**: Enums and custom types
- **Errors**: Custom error classes

Helpers
~~~~~~

Utility classes and functions:

- **Utils**: Various utility functions
- **Interceptors**: Middleware for gRPC, FastAPI, etc.
- **Metaclasses**: Special classes like Singleton

Configs
~~~~~~

Configuration templates for various services:

- **BaseConfig**: Base configuration class
- **SqlAlchemyConfig**: Database configuration
- **RedisConfig**: Redis configuration
- **EmailConfig**: Email service configuration
- **FastAPIConfig**: FastAPI configuration
- **GrpcConfig**: gRPC configuration

Class Diagram
------------

Below is a simplified class diagram of the main components:

.. code-block::

   +-----------------+     +------------------+     +----------------+
   |     Ports       |<----+     Adapters     +---->|    Models      |
   +-----------------+     +------------------+     +----------------+
            ^                       ^                      ^
            |                       |                      |
            |                       |                      |
            v                       v                      v
   +-----------------+     +------------------+     +----------------+
   |    Helpers      |     |     Configs      |     |    Utils       |
   +-----------------+     +------------------+     +----------------+

Hexagonal Architecture
--------------------

ArchiPy follows the Hexagonal Architecture (also known as Ports and Adapters) pattern:

- **Core Domain**: The central part of the application containing business logic
- **Ports**: Interfaces that define how to interact with the domain
- **Adapters**: Implementations of the ports connecting to external systems

Benefits of this architecture:

1. **Separation of Concerns**: Business logic is separate from external systems
2. **Testability**: Easy to mock external dependencies
3. **Flexibility**: Easy to swap out adapters without changing the core domain
4. **Maintainability**: Clean boundaries between components

Dependency Injection
------------------

ArchiPy uses dependency injection to manage dependencies:

.. code-block:: python

   # Example of dependency injection

   class UserService:
       def __init__(self, user_repository):
           self.user_repository = user_repository

   # Adapter implementation
   user_repository = SqlAlchemyAdapter(session_manager, UserEntity)

   # Inject the adapter
   user_service = UserService(user_repository)

Error Handling Strategy
---------------------

ArchiPy provides a comprehensive set of custom errors, all inheriting from a base ``BaseError`` class:

- **Domain Errors**: Errors related to business logic
- **Infrastructure Errors**: Errors related to external systems
- **Validation Errors**: Errors related to data validation

Key Design Principles
-------------------

1. **Explicit is better than implicit**
2. **Composition over inheritance**
3. **Single Responsibility Principle**
4. **Interface Segregation Principle**
5. **Dependency Inversion Principle**
