# Getting Started

This guide will help you start building applications with ArchiPy.

## Basic Setup

1. First, initialize your application with a configuration:

```python
from archipy.configs.base_config import BaseConfig

class AppConfig(BaseConfig):
    # Custom configuration
    pass

# Set as global config
config = AppConfig()
BaseConfig.set_global(config)
```

2. Define your domain models:

```python
from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from archipy.models.entities import BaseEntity

class User(BaseEntity):
    __tablename__ = "users"

    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)

    # Relationships
    posts = relationship("Post", back_populates="author")

class Post(BaseEntity):
    __tablename__ = "posts"

    title = Column(String(255))
    content = Column(String(1000))

    # Foreign keys
    author_id = Column(UUID, ForeignKey("users.test_uuid"))

    # Relationships
    author = relationship("User", back_populates="posts")
```

3. Set up your database adapter:

```python
# For PostgreSQL
from archipy.adapters.postgres.sqlalchemy.adapters import PostgresSQLAlchemyAdapter, AsyncPostgresSQLAlchemyAdapter

# For SQLite
from archipy.adapters.sqlite.sqlalchemy.adapters import SqliteSQLAlchemyAdapter, AsyncSqliteSQLAlchemyAdapter

# For StarRocks
from archipy.adapters.starrocks.sqlalchemy.adapters import StarrocksSQLAlchemyAdapter, AsyncStarrocksSQLAlchemyAdapter

# Create adapter (uses global config)
db_adapter = PostgresSQLAlchemyAdapter()

# Create tables (development only)
BaseEntity.metadata.create_all(db_adapter.session_manager.engine)
```

4. Implement your repositories:

```python
from sqlalchemy import select

class UserRepository:
    def __init__(self, db_adapter):
        self.db_adapter = db_adapter

    def create(self, username, email):
        user = User(test_uuid=uuid4(), username=username, email=email)
        return self.db_adapter.create(user)

    def get_by_username(self, username):
        query = select(User).where(User.username == username)
        users, _ = self.db_adapter.execute_search_query(User, query)
        return users[0] if users else None
```

5. Implement your business logic:

```python
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, username, email):
        # Business logic here (validation, etc.)
        return self.user_repository.create(username, email)
```

## Working with Redis

For caching or other Redis operations:

```python
from archipy.adapters.redis.adapters import RedisAdapter

# Create Redis adapter (uses global config)
redis_adapter = RedisAdapter()

# Cache user data
def cache_user(user):
    user_data = {
        "username": user.username,
        "email": user.email
    }
    redis_adapter.set(f"user:{user.test_uuid}", json.dumps(user_data), ex=3600)

# Get cached user
def get_cached_user(user_id):
    data = redis_adapter.get(f"user:{user_id}")
    return json.loads(data) if data else None
```

## Working with FastAPI

Integrate with FastAPI:

```python
from fastapi import FastAPI, Depends, HTTPException
from archipy.helpers.utils.app_utils import AppUtils

# Create FastAPI app
app = AppUtils.create_fastapi_app(BaseConfig.global_config())

# Create dependencies
def get_user_service():
    user_repo = UserRepository(db_adapter)
    return UserService(user_repo)

# Define routes
@app.post("/users/")
def create_user(username: str, email: str, service: UserService = Depends(get_user_service)):
    try:
        user = service.register_user(username, email)
        return {"id": str(user.test_uuid), "username": user.username}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Examples

### Configuration Management

Standardize and inject configurations:

```python
from archipy.configs.base_config import BaseConfig

# Define a custom config
class MyAppConfig(BaseConfig):
    database_url: str = "sqlite:///example.db"
    redis_host: str = "localhost"

config = MyAppConfig()
print(config.database_url)  # "sqlite:///example.db"
```

### Adapters & Mocks

Use adapters for external systems with mocks for testing:

```python
from archipy.adapters.redis.adapters import AsyncRedisAdapter
from archipy.adapters.redis.mocks import AsyncRedisMock

# Production use
redis = AsyncRedisAdapter()
await redis.set("key", "value", ex=3600)
print(await redis.get("key"))  # "value"

# Testing with mock
mock_redis = AsyncRedisMock()
await mock_redis.set("key", "test")
print(await mock_redis.get("key"))  # "test"
```

### Entities & DTOs

Standardize data models:

```python
from sqlalchemy import Column, Integer, String
from archipy.models.entities.sqlalchemy.base_entities import BaseEntity
from archipy.models.dtos.base_dtos import BaseDTO

# Entity
class User(BaseEntity):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

# DTO
class UserDTO(BaseDTO):
    id: int
    name: str

user = UserDTO(id=1, name="Alice")
print(user.model_dump())  # {'id': 1, 'name': 'Alice'}
```

### Helper Utilities

Simplify tasks with utilities and decorators:

```python
from archipy.helpers.utils.datetime_utils import get_utc_now
from archipy.helpers.decorators.retry import retry

# Utility
now = get_utc_now()
print(now)  # Current UTC time

# Decorator
@retry(max_attempts=3, delay=1)
def risky_operation():
    # Simulated failure
    raise ValueError("Try again")

try:
    risky_operation()
except ValueError as e:
    print(f"Failed after retries: {e}")
```

### BDD Testing

Validate features with `behave`:

```bash
# Run BDD tests
make behave
```

Example feature file (`features/app_utils.feature`):

```gherkin
Feature: Application Utilities
  Scenario: Get UTC time
    When I get the current UTC time
    Then the result should be a valid datetime
```

### Async Operations

Support for asynchronous workflows:

```python
import asyncio
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter

async def fetch_users():
    adapter = AsyncPostgresSQLAlchemyAdapter()
    users = await adapter.execute_search_query(User, pagination=None, sort_info=None)
    return users

users, total = asyncio.run(fetch_users())
print(users)  # List of User entities
```

## Available Commands

Run `make help` for all commands. Common ones:

- **Format Code**: `make format`
- **Lint Code**: `make lint`
- **Run BDD Tests**: `make behave`
- **Build Project**: `make build`
- **Clean Artifacts**: `make clean`
