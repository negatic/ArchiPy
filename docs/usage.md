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
from archipy.models.entities.sqlalchemy.base_entities import BaseEntity

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
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO

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

    def search_users(self, search_term: str | None = None,
                    pagination: PaginationDTO | None = None,
                    sort: SortDTO | None = None):
        query = select(User)
        if search_term:
            query = query.where(User.username.ilike(f"%{search_term}%"))
        return self.db_adapter.execute_search_query(User, query, pagination, sort)
```

5. Implement your business logic:

```python
from archipy.models.errors.custom_errors import AlreadyExistsError

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, username, email):
        # Check if user exists
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise AlreadyExistsError(
                resource_type="user",
                additional_data={"username": username}
            )

        # Create new user
        return self.user_repository.create(username, email)
```

## Working with Redis

For caching or other Redis operations:

```python
from archipy.adapters.redis.adapters import RedisAdapter, AsyncRedisAdapter

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

## Working with Keycloak

For authentication and authorization:

```python
from archipy.adapters.keycloak.adapters import KeycloakAdapter, AsyncKeycloakAdapter

# Create Keycloak adapter (uses global config)
keycloak = KeycloakAdapter()

# Authenticate user
token = keycloak.get_token("username", "password")

# Validate token
is_valid = keycloak.validate_token(token["access_token"])

# Get user info
user_info = keycloak.get_userinfo(token["access_token"])
```

## Working with MinIO

For object storage operations:

```python
from archipy.adapters.minio.adapters import MinioAdapter

# Create MinIO adapter (uses global config)
minio = MinioAdapter()

# Create bucket
if not minio.bucket_exists("my-bucket"):
    minio.make_bucket("my-bucket")

# Upload file
minio.put_object("my-bucket", "document.pdf", "/path/to/file.pdf")

# Generate download URL
download_url = minio.presigned_get_object("my-bucket", "document.pdf", expires=3600)
```

## Working with FastAPI

Integrate with FastAPI:

```python
from fastapi import FastAPI, Depends, HTTPException
from archipy.helpers.utils.app_utils import AppUtils
from archipy.helpers.utils.keycloak_utils import KeycloakUtils
from archipy.models.errors.custom_errors import BaseError

# Create FastAPI app
app = AppUtils.create_fastapi_app(BaseConfig.global_config())

# Create dependencies
def get_user_service():
    user_repo = UserRepository(db_adapter)
    return UserService(user_repo)

# Define routes with authentication
@app.post("/users/")
def create_user(
    username: str,
    email: str,
    service: UserService = Depends(get_user_service),
    user: dict = Depends(KeycloakUtils.fastapi_auth(required_roles={"admin"}))
):
    try:
        user = service.register_user(username, email)
        return {"id": str(user.test_uuid), "username": user.username}
    except BaseError as e:
        raise HTTPException(
            status_code=e.http_status_code or 400,
            detail=e.to_dict()
        )
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
    keycloak_url: str = "http://localhost:8080"
    minio_endpoint: str = "localhost:9000"

config = MyAppConfig()
print(config.database_url)  # "sqlite:///example.db"
```

### Database Operations

Use database adapters with transactions:

```python
from archipy.helpers.decorators.sqlalchemy_atomic import (
    postgres_sqlalchemy_atomic_decorator,
    async_postgres_sqlalchemy_atomic_decorator,
    sqlite_sqlalchemy_atomic_decorator,
    async_sqlite_sqlalchemy_atomic_decorator,
    starrocks_sqlalchemy_atomic_decorator,
    async_starrocks_sqlalchemy_atomic_decorator
)

# Synchronous PostgreSQL transaction
@postgres_sqlalchemy_atomic_decorator
def create_user_with_posts(username, email, posts):
    user = User(username=username, email=email)
    db_adapter.create(user)

    for post in posts:
        post.author_id = user.test_uuid
        db_adapter.create(post)

    return user

# Asynchronous PostgreSQL transaction
@async_postgres_sqlalchemy_atomic_decorator
async def async_create_user_with_posts(username, email, posts):
    user = User(username=username, email=email)
    await db_adapter.create(user)

    for post in posts:
        post.author_id = user.test_uuid
        await db_adapter.create(post)

    return user

# Synchronous SQLite transaction
@sqlite_sqlalchemy_atomic_decorator
def create_sqlite_user(username, email):
    user = User(username=username, email=email)
    return db_adapter.create(user)

# Asynchronous SQLite transaction
@async_sqlite_sqlalchemy_atomic_decorator
async def async_create_sqlite_user(username, email):
    user = User(username=username, email=email)
    return await db_adapter.create(user)

# Synchronous StarRocks transaction
@starrocks_sqlalchemy_atomic_decorator
def create_starrocks_user(username, email):
    user = User(username=username, email=email)
    return db_adapter.create(user)

# Asynchronous StarRocks transaction
@async_starrocks_sqlalchemy_atomic_decorator
async def async_create_starrocks_user(username, email):
    user = User(username=username, email=email)
    return await db_adapter.create(user)
```

### Helper Utilities

Simplify tasks with utilities and decorators:

```python
from archipy.helpers.utils.datetime_utils import get_utc_now
from archipy.helpers.decorators.retry import retry
from archipy.helpers.decorators.singleton import singleton

# Utility
now = get_utc_now()
print(now)  # Current UTC time

# Retry decorator
@retry(max_attempts=3, delay=1)
def risky_operation():
    # Simulated failure
    raise ValueError("Try again")

# Singleton decorator
@singleton
class DatabaseManager:
    def __init__(self):
        self.adapter = PostgresSQLAlchemyAdapter()
```

### Async Operations

Support for asynchronous workflows:

```python
import asyncio
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter

async def fetch_users():
    adapter = AsyncPostgresSQLAlchemyAdapter()
    users, total = await adapter.execute_search_query(
        User,
        pagination=PaginationDTO(page=1, size=10),
        sort=SortDTO(field="username", order="asc")
    )
    return users

users = asyncio.run(fetch_users())
print(users)  # List of User entities
```

## Available Commands

Run `make help` for all commands. Common ones:

- **Format Code**: `make format`
- **Lint Code**: `make lint`
- **Run BDD Tests**: `make behave`
- **Build Project**: `make build`
- **Clean Artifacts**: `make clean`
