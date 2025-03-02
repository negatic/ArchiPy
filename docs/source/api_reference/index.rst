.. _api_reference:

API Reference
=============

This section documents ArchiPy’s modules and classes, designed to support a standardized, testable, and scalable Python architecture. The API reflects the project’s core goals:

- **Configuration Management**: Standardized config handling and injection.
- **Adapters & Mocks**: Interfaces and implementations for external systems with testing mocks.
- **Data Standardization**: Base entities, DTOs, and types for consistency.
- **Helper Utilities**: Tools, decorators, and interceptors for productivity.
- **BDD Support**: Integrated with testing utilities (see `features/` for examples).
- **Best Practices**: Structured for modern Python development.

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   adapters
   configs
   helpers
   models
   utils

Adapters
-------

:doc:`adapters`

The adapters module contains implementations of ports that connect the application to external systems:

- ORM adapters for database operations
- Redis adapters for caching
- Email adapters for sending emails
- gRPC adapters for microservice communication

Configs
------

:doc:`configs`

The configs module contains configuration templates for various services:

- Base configuration
- SQLAlchemy configuration
- Redis configuration
- Email configuration
- FastAPI configuration
- gRPC configuration

Helpers
------

:doc:`helpers`

The helpers module contains utility classes and functions:

- Interceptors for gRPC and FastAPI
- Metaclasses (e.g., Singleton)
- Utility functions

Models
-----

:doc:`models`

The models module contains data structures:

- DTOs (Data Transfer Objects)
- Entities (database models)
- Custom errors
- Type definitions

Utils
----

:doc:`utils`

The utils module contains utility functions for various tasks:

- Datetime utilities
- String utilities
- File utilities
- JWT utilities
- Password utilities
