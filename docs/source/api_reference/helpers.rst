.. _api_helpers:

Helpers
=======

The ``helpers`` module provides utility functions and classes to simplify common development tasks.

Submodules
----------

Utils
~~~~~

.. toctree::
   :maxdepth: 2

   helpers/utils

General utility functions for common operations:

- String manipulation
- Date and time handling
- Error utilities
- File operations
- Password utilities
- JWT token handling
- TOTP generation

Decorators
~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   helpers/decorators

Function and class decorators for:

- Method deprecation
- Class deprecation
- Timing operations
- Retry logic

Interceptors
~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   helpers/interceptors

Classes for cross-cutting concerns:

- Logging
- Performance monitoring
- Request/response tracking

Validators
~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   helpers/validators

Data validation utilities for:

- Input validation
- Schema validation
- Business rule validation

Overview
--------

The helpers module offers utilities, decorators, and interceptors to enhance productivity and simplify common development tasks, such as retry logic, rate limiting, and tracing.

**See Examples**: :ref:`examples_helpers`

Decorators
----------

.. admonition:: Example Usage
   :class: tip

   See :ref:`examples_helpers_decorators` for practical examples of decorators.

.. automodule:: archipy.helpers.decorators.retry
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.helpers.decorators.singleton
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.helpers.decorators.sqlalchemy_atomic
   :members:
   :undoc-members:
   :show-inheritance:

Interceptors
------------

FastAPI Interceptors
~~~~~~~~~~~~~~~~~~~~

.. automodule:: archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler
   :members:
   :undoc-members:
   :show-inheritance:

gRPC Interceptors
~~~~~~~~~~~~~~~~~

.. automodule:: archipy.helpers.interceptors.grpc.trace.grpc_client_trace_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.helpers.interceptors.grpc.trace.grpc_server_trace_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

Metaclasses
-----------

.. automodule:: archipy.helpers.metaclasses.singleton
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
-----------

Retry Decorator
~~~~~~~~~~~~~~~

.. autofunction:: archipy.helpers.decorators.retry.retry

Singleton
~~~~~~~~~

.. autoclass:: archipy.helpers.metaclasses.singleton.Singleton
   :members:
   :undoc-members:
   :show-inheritance:

FastAPIRestRateLimitHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler.FastAPIRestRateLimitHandler
   :members:
   :undoc-members:
   :show-inheritance:
