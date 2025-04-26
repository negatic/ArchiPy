# PostgreSQL Adapter

This example demonstrates how to use the PostgreSQL adapter for database operations.

## Basic Usage

```python
from archipy.adapters.postgres.sqlalchemy.adapters import PostgresSQLAlchemyAdapter
from archipy.models.entities.sqlalchemy.base_entities import BaseEntity
from sqlalchemy import Column, String

# Define a model
class User(BaseEntity):
    __tablename__ = "users"
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)

# Create adapter
adapter = PostgresSQLAlchemyAdapter()

# Create tables
BaseEntity.metadata.create_all(adapter.session_manager.engine)

# Basic operations
with adapter.session() as session:
    # Create
    user = User(username="john_doe", email="john@example.com")
    session.add(user)
    session.commit()

    # Read
    user = session.query(User).filter_by(username="john_doe").first()
    print(user.email)  # john@example.com

    # Update
    user.email = "john.doe@example.com"
    session.commit()

    # Delete
    session.delete(user)
    session.commit()
```

## Using Transactions

```python
from archipy.helpers.decorators.sqlalchemy_atomic import postgres_sqlalchemy_atomic_decorator

@postgres_sqlalchemy_atomic_decorator
def create_user_with_profile(username, email, profile_data):
    user = User(username=username, email=email)
    adapter.create(user)

    profile = Profile(user_id=user.test_uuid, **profile_data)
    adapter.create(profile)

    return user
```

## Async Operations

```python
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

async def main():
    adapter = AsyncPostgresSQLAlchemyAdapter()

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_user_async(username, email):
        user = User(username=username, email=email)
        return await adapter.create(user)

    user = await create_user_async("jane_doe", "jane@example.com")
    print(user.username)  # jane_doe
```

## Error Handling

```python
from archipy.models.errors.custom_errors import (
    AlreadyExistsError,
    NotFoundError,
    InternalError
)

try:
    user = adapter.get_by_id(User, user_id)
    if not user:
        raise NotFoundError(resource_type="user")
except AlreadyExistsError as e:
    print(f"User already exists: {e.message}")
except InternalError as e:
    print(f"Database error: {e.message}")
```
