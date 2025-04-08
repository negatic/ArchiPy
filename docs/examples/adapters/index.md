# Adapter Examples

ArchiPy provides a variety of adapters to help interface with external systems, maintaining a clean separation between your business logic and external dependencies.

## Available Adapters

| Adapter | Purpose | Example | API Reference |
|---------|---------|---------|---------------|
| [Email](email.md) | Email sending interface | Connect to SMTP servers for sending emails | [API](../../api_reference/adapters.md#email) |
| [Keycloak](keycloak.md) | Authentication & authorization | User management and access control with Keycloak | [API](../../api_reference/adapters.md#keycloak) |
| [Minio](minio.md) | Object storage | S3-compatible object storage for files and documents | [API](../../api_reference/adapters.md#minio) |
| [ORM](orm.md) | Database access | SQLAlchemy integration for database operations | [API](../../api_reference/adapters.md#orm) |
| [Redis](redis.md) | Key-value store | Caching, pub/sub, and data storage with Redis | [API](../../api_reference/adapters.md#redis) |

## Adapter Architecture

ArchiPy follows the ports and adapters pattern (hexagonal architecture):

```
┌────────────────────────────────────────┐
│             Domain Logic               │
└───────────────────┬────────────────────┘
                    │ uses
┌───────────────────▼────────────────────┐
│                 Ports                  │
│          (Abstract Interfaces)         │
└───────────────────┬────────────────────┘
                    │ implemented by
┌───────────────────▼────────────────────┐
│                Adapters                │
│         (Concrete Implementations)     │
└───────────────────┬────────────────────┘
                    │ connects to
┌───────────────────▼────────────────────┐
│            External Systems            │
│   (Databases, APIs, Message Queues)    │
└────────────────────────────────────────┘
```

## Testing with Mock Adapters

Each adapter in ArchiPy comes with a corresponding mock implementation for testing:

```python
# Production code
from archipy.adapters.redis import RedisAdapter

redis = RedisAdapter(host="redis.example.com", port=6379)
redis.set("key", "value")

# Test code
from archipy.adapters.redis import RedisMock

redis_mock = RedisMock()
redis_mock.set("key", "test_value")
assert redis_mock.get("key") == "test_value"
```

## Creating Custom Adapters

Creating custom adapters is straightforward:

1. Define a port (abstract interface)
2. Implement the adapter class
3. Optionally create a mock implementation

See the [Architecture](../../architecture.md) guide for more details on creating custom adapters.
