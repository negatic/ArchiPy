.. _api_helpers:

Helpers
======

Overview
--------

The helpers module contains utility classes and functions for various tasks.


Interceptors
~~~~~~~~~~

FastAPI Interceptors
^^^^^^^^^^^^^^^^^^

.. automodule:: archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler
   :members:
   :undoc-members:
   :show-inheritance:

gRPC Interceptors
^^^^^^^^^^^^^^^

Base
''''

.. automodule:: archipy.helpers.interceptors.grpc.base.base_grpc_client_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.helpers.interceptors.grpc.base.base_grpc_server_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

Metrics
'''''''

.. automodule:: archipy.helpers.interceptors.grpc.metric.grpc_server_metric_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

Tracing
'''''''

.. automodule:: archipy.helpers.interceptors.grpc.trace.grpc_client_trace_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.helpers.interceptors.grpc.trace.grpc_server_trace_interceptor
   :members:
   :undoc-members:
   :show-inheritance:

Metaclasses
~~~~~~~~~

.. automodule:: archipy.helpers.metaclasses.singleton
   :members:
   :undoc-members:
   :show-inheritance:

Utils
~~~~

.. automodule:: archipy.helpers.utils.app_utils
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.helpers.utils.base_utils
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
---------

FastAPI Rate Limit Handler
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler.FastAPIRestRateLimitHandler
   :members:
   :undoc-members:
   :show-inheritance:

gRPC Client Interceptors
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.helpers.interceptors.grpc.base.base_grpc_client_interceptor.BaseGrpcClientInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.interceptors.grpc.base.base_grpc_client_interceptor.BaseAsyncGrpcClientInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.interceptors.grpc.trace.grpc_client_trace_interceptor.GrpcClientTraceInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.interceptors.grpc.trace.grpc_client_trace_interceptor.AsyncGrpcClientTraceInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

gRPC Server Interceptors
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.helpers.interceptors.grpc.base.base_grpc_server_interceptor.BaseGrpcServerInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.interceptors.grpc.trace.grpc_server_trace_interceptor.GrpcServerTraceInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.interceptors.grpc.metric.grpc_server_metric_interceptor.GrpcServerMetricInterceptor
   :members:
   :undoc-members:
   :show-inheritance:

Singleton Metaclass
~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.helpers.metaclasses.singleton.Singleton
   :members:
   :undoc-members:
   :show-inheritance:

Application Utils
~~~~~~~~~~~~~~

.. autoclass:: archipy.helpers.utils.app_utils.AppUtils
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.utils.app_utils.FastAPIUtils
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.helpers.utils.app_utils.FastAPIExceptionHandler
   :members:
   :undoc-members:
   :show-inheritance:
