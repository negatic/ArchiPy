.. _api_reference:

API Reference
============

This section provides detailed API documentation for ArchiPy's modules and components.

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
