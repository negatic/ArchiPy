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

::: archipy.adapters.email.email_adapter
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.email.email_port
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

::: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.orm.sqlalchemy.session_manager_adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.orm.sqlalchemy.sqlalchemy_ports
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

::: archipy.adapters.redis.redis_adapters
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.redis.redis_ports
    options:
      show_root_heading: true
      show_source: true

::: archipy.adapters.redis.redis_mocks
    options:
      show_root_heading: true
      show_source: true