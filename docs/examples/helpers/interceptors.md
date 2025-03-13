# Interceptor Examples

This page demonstrates how to use ArchiPy's interceptors.

## Basic Usage

```python
from archipy.helpers.interceptors.grpc.trace import GrpcServerTraceInterceptor

# Create a gRPC server with tracing
tracer = GrpcServerTraceInterceptor()
server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10),
    interceptors=[tracer]
)
```

This documentation is being migrated from Sphinx to MkDocs format.
Please check back soon for complete content.
