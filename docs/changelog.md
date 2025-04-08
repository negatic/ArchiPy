# Changelog

All notable changes to ArchiPy are documented in this changelog, organized by version.

## [0.13.1] - 2025-04-08

### Added

- Comprehensive docstrings for all configuration classes
- Improved documentation for utility functions
- Additional validation and error handling throughout codebase

### Changed

- Enhanced error handling with more specific exception types
- Improved type safety with explicit typing and casting
- Better parameter naming and consistency across modules

### Security

- Replaced `random` module with `secrets` for all cryptographic operations
- Improved TOTP implementation with better security practices
- Enhanced password utilities with better validation and generation


## [0.13.0] - 2025-04-08

### Overview

Version 0.13.0 introduces a comprehensive MinIO adapter for S3-compatible object storage integration, complete with extensive documentation, BDD testing, and performance optimizations.

### Key Features

- **Complete MinIO Integration**: Full-featured adapter with support for all common S3 operations
- **Robust Error Handling**: Domain-specific exceptions for consistent error management
- **Performance Optimizations**: Built-in TTL caching for frequently accessed operations
- **Comprehensive Documentation**: Extensive examples covering all adapter functionality
- **Behavior-Driven Testing**: Complete BDD test suite ensuring reliability

### Added

- **MinIO Adapter Implementation**:
  - Port definition with 12 standardized methods for S3 operations
  - Complete implementation using the official MinIO Python client
  - TTL caching for performance optimization
  - Clear cache management with `clear_all_caches` method

- **Configuration**:
  - MinioConfig class with endpoint, credentials, and connection settings

- **Testing Infrastructure**:
  - BDD testing for bucket and object operations
  - Presigned URL generation and validation tests
  - Bucket policy management tests

### Changed

- Refactored MinIO adapter with improved error handling
- Updated documentation with comprehensive examples

### Usage Examples

```python
# Initialize the MinIO adapter
from archipy.adapters.minio.adapters import MinioAdapter
minio = MinioAdapter()

# Create a bucket and upload a file
minio.make_bucket("my-bucket")
minio.put_object("my-bucket", "document.pdf", "/path/to/document.pdf")

# Generate a presigned URL for temporary access
download_url = minio.presigned_get_object("my-bucket", "document.pdf", expires=3600)
```

## [0.12.0] - 2025-03-29

### Overview

Version 0.12.0 introduces Keycloak integration utilities for seamless authentication and authorization in FastAPI applications. The release also includes enhanced error handling and refactoring of error message types.

### Key Features

- **Keycloak Authentication**: Utilities for authenticating users with Keycloak in FastAPI
- **Role-Based Authorization**: Support for role-based access control with customizable requirements
- **Resource-Based Authorization**: Fine-grained control for resource access based on ownership
- **Asynchronous Support**: Both sync and async implementations for all authentication flows

### Added

- **KeycloakUtils Class**:
  - `fastapi_auth()`: Decorator for authentication in FastAPI endpoints
  - `async_fastapi_auth()`: Asynchronous version of the authentication decorator
  - Token validation and introspection
  - User info extraction
  - Resource-based authorization
  - Role-based access control

### Changed

- Renamed `ExceptionMessageType` to `ErrorMessageType` for better semantic clarity
- Enhanced error documentation with detailed descriptions
- Updated error handling code to use the new error message types

### Usage Examples

```python
from fastapi import FastAPI, Depends
from archipy.helpers.utils.keycloak_utils import KeycloakUtils

app = FastAPI()

@app.get("/api/profile")
def get_profile(user: dict = Depends(KeycloakUtils.fastapi_auth(
    required_roles={"user"},
    admin_roles={"admin"}
))):
    return {
        "user_id": user.get("sub"),
        "username": user.get("preferred_username")
    }
```

```python
@app.get("/api/users/{user_uuid}/info")
def get_user_info(
    user_uuid: UUID,
    user_info: dict = Depends(KeycloakUtils.fastapi_auth(
        resource_type_param="user_uuid",
        resource_type="users",
        required_roles={"user"},
        admin_roles={"admin", "superadmin"}
    ))
):
    # Users can only access their own info unless they have admin role
    return {
        "message": f"User info for {user_uuid}",
        "username": user_info.get("preferred_username")
    }
```

## [0.11.2] - 2025-03-21

### Overview

Version 0.11.2 provides enhanced error handling and bug fixes.

### Key Features

- **Error Handling Improvements**: Enhanced exception management
- **Better Error Reporting**: Improved error messaging

### Fixed

- Bug fixes for error handling
- Improved error reporting and messaging

## [0.11.1] - 2025-03-15

### Overview

Version 0.11.1 delivers performance enhancements and optimizations.

### Key Features

- **Performance Enhancements**: Optimized resource usage
- **Improved Caching**: Better caching mechanisms

### Fixed

- Performance optimizations
- Improved resource utilization

## [0.11.0] - 2025-03-10

### Overview

Version 0.11.0 introduces the Keycloak adapter with authentication and authorization features.

### Key Features

- **Keycloak Integration**: Authentication and authorization
- **Asynchronous Adapters**: Async support for Keycloak operations
- **TTL Cache Decorator**: Time-based caching for performance

### Added

- Asynchronous Keycloak adapter
- TTL cache decorator for improved performance
- Keycloak documentation and examples

### Changed

- Refactored Keycloak adapter for better performance

### Usage Examples

```python
from archipy.adapters.keycloak.adapters import KeycloakAdapter

# Initialize adapter with configuration from global config
keycloak = KeycloakAdapter()

# Authenticate and get access token
token = keycloak.get_token("username", "password")

# Get user information
user_info = keycloak.get_userinfo(token)

# Verify token validity
is_valid = keycloak.validate_token(token)
```

## [0.10.2] - 2025-03-05

### Overview

Version 0.10.2 provides stability improvements and bug fixes for the Redis adapter.

### Key Features

- **Redis Stability Fixes**: Connection pool improvements
- **Error Handling Enhancements**: Better error recovery

### Fixed

- Connection pool stability issues
- Error handling enhancements

## [0.10.1] - 2025-03-01

### Overview

Version 0.10.1 expands documentation and improves examples.

### Key Features

- **Documentation Updates**: Improved examples
- **API Reference Expansion**: More detailed API documentation

### Added

- Enhanced documentation for Redis and email adapters
- Improved examples for common operations

## [0.10.0] - 2025-02-25

### Overview

Version 0.10.0 adds Redis caching and email service integration.

### Key Features

- **Redis Integration**: Caching and key-value storage
- **Email Service Adapter**: Email sending capabilities
- **Enhanced Configuration**: Improved configuration management

### Added

- Redis adapter for caching and key-value storage
- Email service adapter for sending emails
- Configuration improvements

### Usage Examples

```python
# Initialize the Redis adapter
from archipy.adapters.redis.adapters import RedisAdapter
redis = RedisAdapter()

# Basic operations
redis.set("user:1:name", "John Doe")
name = redis.get("user:1:name")

# Using with TTL
redis.set("session:token", "abc123", ttl=3600)  # Expires in 1 hour
```

## [0.9.0] - 2025-02-20

### Overview

Version 0.9.0 adds Time-based One-Time Password (TOTP) security features.

### Key Features

- **TOTP Security**: Time-based one-time passwords
- **Multi-factor Authentication**: Enhanced security with MFA
- **Secure Token Generation**: Cryptographically secure tokens

### Added

- TOTP generation and validation
- Secure token generation utilities
- Multi-factor authentication support

### Usage Examples

```python
from archipy.helpers.utils.totp_utils import TOTPUtils
from uuid import uuid4

# Generate a TOTP code
user_id = uuid4()
totp_code, expires_at = TOTPUtils.generate_totp(user_id)

# Verify a TOTP code
is_valid = TOTPUtils.verify_totp(user_id, totp_code)

# Generate a secure key for TOTP initialization
secret_key = TOTPUtils.generate_secret_key_for_totp()
```

## [0.8.0] - 2025-02-15

### Overview

Version 0.8.0 introduces Redis adapter implementation with mock testing utilities.

### Key Features

- **Redis Adapter**: Key-value store and caching
- **Mock Implementation**: Testing utilities for Redis
- **Caching Functionality**: Performance optimizations

### Added

- Redis adapter with comprehensive API
- Mock implementation for testing
- Documentation for Redis integration

### Fixed

- Various documentation and configuration issues

## [0.7.2] - 2025-02-10

### Overview

Version 0.7.2 provides stability improvements and bug fixes for the SQLAlchemy adapter.

### Key Features

- **Connection Pool Stability**: Improved pool management
- **Transaction Handling**: Better transaction management
- **Error Handling**: Enhanced error reporting

### Fixed

- Connection pool stability and management
- Transaction handling and isolation
- Error reporting for database operations

## [0.7.1] - 2025-02-05

### Overview

Version 0.7.1 provides performance optimizations for the SQLAlchemy ORM integration.

### Key Features

- **Query Efficiency**: Improved query performance
- **Memory Optimization**: Reduced memory usage
- **Connection Handling**: Enhanced connection management

### Fixed

- Improved query efficiency and performance
- Reduced memory usage for ORM operations
- Enhanced connection handling and management

## [0.7.0] - 2025-02-01

### Overview

Version 0.7.0 introduces SQLAlchemy ORM integration with transaction management and connection pooling.

### Key Features

- **SQLAlchemy ORM Integration**: Database adapter implementation
- **Model Integration**: ORM entity model structure
- **Transaction Management**: Atomic transaction support

### Added

- SQLAlchemy adapter implementation for database operations
- Base entity models for ORM integration
- Transaction management and connection pooling

### Usage Examples

```python
from archipy.adapters.orm.sqlalchemy.adapters import SQLAlchemyAdapter
from archipy.models.entities.sqlalchemy.base_entities import BaseEntity
from sqlalchemy import Column, String

# Initialize ORM adapter
orm = SQLAlchemyAdapter()

# Define models
class User(BaseEntity):
    __tablename__ = "users"
    name = Column(String(100))
    email = Column(String(100), unique=True)

# Perform operations
with orm.session() as session:
    # Create
    new_user = User(name="John Doe", email="john@example.com")
    session.add(new_user)
    session.commit()

    # Read
    user = session.query(User).filter_by(email="john@example.com").first()
```

## [0.6.1] - 2025-01-25

### Overview

Version 0.6.1 provides stability improvements and bug fixes for the gRPC interceptors.

### Key Features

- **Stability Improvements**: Bug fixes for interceptors
- **Memory Management**: Fixed memory leaks
- **Performance Optimization**: Improved interceptor efficiency

### Fixed

- Bug fixes for gRPC interceptors
- Memory leak fixes in request/response handling
- Performance optimizations for interceptors

## [0.6.0] - 2025-01-20

### Overview

Version 0.6.0 introduces gRPC interceptors for request/response interception and monitoring.

### Key Features

- **gRPC Interceptors**: Client and server interceptors
- **Tracing and Monitoring**: Request/response monitoring
- **Error Handling**: Enhanced gRPC error management

### Added

- Client and server gRPC interceptors
- Tracing and monitoring capabilities
- Error handling middleware for gRPC

## [0.5.1] - 2025-01-15

### Overview

Version 0.5.1 provides stability improvements and bug fixes for the FastAPI integration.

### Key Features

- **Stability Improvements**: Bug fixes and enhancements
- **Response Handling**: Improved response processing
- **Error Management**: Enhanced error handling

### Fixed

- Bug fixes for FastAPI middleware components
- Improved response handling and error management
- Performance optimizations for request processing

## [0.5.0] - 2025-01-10

### Overview

Version 0.5.0 adds FastAPI integration with middleware components and request/response handlers.

### Key Features

- **FastAPI Integration**: Utilities for FastAPI applications
- **Middleware Components**: Request and response middleware
- **Error Handling**: Standardized error management

### Added

- FastAPI integration utilities and components
- Middleware for request and response processing
- Standardized error handling and response formatting

## [0.4.0] - 2025-01-05

### Overview

Version 0.4.0 introduces a comprehensive configuration management system with environment variable support.

### Key Features

- **Configuration System**: Flexible configuration with environment variables
- **Validation**: Configuration validation and type checking
- **Default Values**: Sensible defaults with override capability

### Added

- Environment-based configuration with variable support
- Configuration validation and type checking
- Default value management with override capability

## [0.3.0] - 2024-12-25

### Overview

Version 0.3.0 adds core utility functions and helpers to streamline common development tasks.

### Key Features

- **Helper Functions**: Utilities for common tasks
- **Date/Time Handling**: Date and time manipulation utilities
- **String Operations**: String processing and formatting

### Added

- Core utility classes and functions
- Date and time manipulation utilities with timezone support
- String processing and formatting functions

## [0.2.0] - 2024-12-20

### Overview

Version 0.2.0 establishes the foundational architecture for ArchiPy, implementing core design patterns and base structures.

### Key Features

- **Architecture Foundation**: Implementation of the hexagonal architecture
- **Base Models and Entities**: Core data structures and entities
- **Design Patterns**: Implementation of key design patterns

### Added

- Base entity models for data persistence
- Core architectural components following ports and adapters pattern
- Foundational utility classes

## [0.1.0] - 2025-02-21

### Overview

Version 0.1.0 is the initial release of ArchiPy, introducing the core project structure and basic functionality.

### Key Features

- **Project Structure**: Initial repository structure and organization
- **Core Functionality**: Basic framework components and utilities
- **CI/CD Setup**: GitHub Actions workflow for continuous integration

### Added

- Initial project structure with adapters, models, and helpers
- Basic configuration system
- GitHub Actions for automated testing and publishing
