# Helpers

The `helpers` module provides utility functions and classes to simplify common development tasks.

## Submodules

### Utils

*See [helpers/utils](helpers/utils.md) for full documentation.*

General utility functions for common operations:

- String manipulation
- Date and time handling
- Error utilities
- File operations
- Password utilities
- JWT token handling
- TOTP generation

### Decorators

*See [helpers/decorators](helpers/decorators.md) for full documentation.*

Function and class decorators for:

- Method deprecation
- Class deprecation
- Timing operations
- Retry logic

### Interceptors

*See [helpers/interceptors](helpers/interceptors.md) for full documentation.*

Classes for cross-cutting concerns:

- Logging
- Performance monitoring
- Request/response tracking

### Validators

*See [helpers/validators](helpers/validators.md) for full documentation.*

Data validation utilities for:

- Input validation
- Schema validation
- Business rule validation

## Overview

The helpers module offers utilities, decorators, and interceptors to enhance productivity and simplify common development tasks, such as retry logic, rate limiting, and tracing.

**See Examples**: [Examples Helpers](#examples_helpers)

## Decorators

> **Tip**: See [Examples Helpers Decorators](#examples_helpers_decorators) for practical examples of decorators.

### Retry Decorator

Documentation for `archipy.helpers.decorators.retry`.  
*Includes all members, undocumented members, and shows inheritance.*

### Singleton Decorator

Documentation for `archipy.helpers.decorators.singleton`.  
*Includes all members, undocumented members, and shows inheritance.*

### SQLAlchemy Atomic Decorator

Documentation for `archipy.helpers.decorators.sqlalchemy_atomic`.  
*Includes all members, undocumented members, and shows inheritance.*

## Interceptors

### FastAPI Interceptors

#### FastAPI Rest Rate Limit Handler

Documentation for `archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler`.  
*Includes all members, undocumented members, and shows inheritance.*

### gRPC Interceptors

#### gRPC Client Trace Interceptor

Documentation for `archipy.helpers.interceptors.grpc.trace.grpc_client_trace_interceptor`.  
*Includes all members, undocumented members, and shows inheritance.*

#### gRPC Server Trace Interceptor

Documentation for `archipy.helpers.interceptors.grpc.trace.grpc_server_trace_interceptor`.  
*Includes all members, undocumented members, and shows inheritance.*

## Metaclasses

### Singleton Metaclass

Documentation for `archipy.helpers.metaclasses.singleton`.  
*Includes all members, undocumented members, and shows inheritance.*

## Key Classes

### Retry Decorator

Function: `archipy.helpers.decorators.retry.retry`  
*See documentation for details.*

### Singleton

Class: `archipy.helpers.metaclasses.singleton.Singleton`  
*Includes all members, undocumented members, and shows inheritance.*

### FastAPIRestRateLimitHandler

Class: `archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler.FastAPIRestRateLimitHandler`  
*Includes all members, undocumented members, and shows inheritance.*