# Adapters

The `adapters` module provides standardized interfaces to external systems and services. It follows the ports and adapters pattern (also known as hexagonal architecture) to decouple application logic from external dependencies.

## Key Features

- **Consistent interfaces** for all external services
- **Built-in mock implementations** for testing
- **Port definitions** for dependency inversion
- **Ready-to-use implementations** for common services

## Available Adapters

### Email

Email sending functionality with standardized interface.

```python
from archipy.adapters.email import EmailAdapter, EmailPort

# Configure email adapter
email_adapter = EmailAdapter(host="smtp.example.com", port=587, username="user", password="pass")

# Send an email
email_adapter.send_email(
    subject="Test Email",
    body="This is a test email",
    recipients=["recipient@example.com"],
)
```

::: archipy.adapters.email.adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.email.ports
    options:
      show_root_heading: true
      show_source: true

### Keycloak

Keycloak integration for authentication and authorization services.

```python
from archipy.adapters.keycloak import KeycloakAdapter, AsyncKeycloakAdapter

# Create a Keycloak adapter (synchronous)
keycloak = KeycloakAdapter()  # Uses global config by default

# Authenticate a user
token = keycloak.get_token("username", "password")

# Validate token
is_valid = keycloak.validate_token(token["access_token"])

# Check user roles
has_admin = keycloak.has_role(token["access_token"], "admin")

# Async usage example
import asyncio

async def auth_example():
    # Create async Keycloak adapter
    async_keycloak = AsyncKeycloakAdapter()

    # Get token asynchronously
    token = await async_keycloak.get_token("username", "password")

    # Get user info
    user_info = await async_keycloak.get_userinfo(token["access_token"])
    return user_info

# Run the async example
user_info = asyncio.run(auth_example())
```

For detailed examples and usage guidelines, see the [Keycloak Adapter Examples](../examples/adapters/keycloak.md).

::: archipy.adapters.keycloak.adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.keycloak.ports
    options:
      show_root_heading: true
      show_source: true

### MinIO

MinIO integration for S3-compatible object storage operations.

```python
from archipy.adapters.minio import MinioAdapter

# Create a MinIO adapter
minio = MinioAdapter()  # Uses global config by default

# Create a bucket
if not minio.bucket_exists("my-bucket"):
    minio.make_bucket("my-bucket")

# Upload a file
minio.put_object("my-bucket", "document.pdf", "/path/to/local/file.pdf")

# Generate a download URL (valid for 1 hour)
download_url = minio.presigned_get_object("my-bucket", "document.pdf")
```

For detailed examples and usage guidelines, see the [MinIO Adapter Examples](../examples/adapters/minio.md).

::: archipy.adapters.minio.adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.minio.ports
    options:
      show_root_heading: true
      show_source: true

### ORM

Object-Relational Mapping adapters, primarily for SQLAlchemy integration.

```python
from archipy.adapters.orm.sqlalchemy import SQLAlchemyAdapter, SQLAlchemySessionManager

# Create session manager
session_manager = SQLAlchemySessionManager(connection_string="postgresql://user:pass@localhost/db")

# Create an ORM adapter
orm_adapter = SQLAlchemyAdapter(session_manager=session_manager)

# Use the adapter
users = orm_adapter.query(User).filter(User.active == True).all()
```

#### SQLAlchemy Components

::: archipy.adapters.orm.sqlalchemy.adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.orm.sqlalchemy.session_manager_adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.orm.sqlalchemy.ports
    options:
      show_root_heading: true
      show_source: true

### Redis

Redis integration for caching and key-value storage.

```python
from archipy.adapters.redis import RedisAdapter, AsyncRedisAdapter

# Create a Redis adapter
redis = RedisAdapter(host="localhost", port=6379, db=0)

# Set value
redis.set("key", "value", ex=3600)  # expires in 1 hour

# Get value
value = redis.get("key")
```

::: archipy.adapters.redis.adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.redis.ports
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.redis.mocks
    options:
      show_root_heading: true
      show_source: true
