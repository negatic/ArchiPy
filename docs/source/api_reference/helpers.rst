.. _api_helpers:

Helpers
=======

Overview
--------

The helpers module offers utilities, decorators, and interceptors to enhance productivity and simplify common development tasks, such as retry logic, rate limiting, and tracing.

Decorators
----------

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
