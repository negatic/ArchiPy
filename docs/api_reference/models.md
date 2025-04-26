# Models

The `models` module provides core data structures and types used throughout the application, following clean architecture principles.

## DTOs (Data Transfer Objects)

### Base DTOs

Base classes for all DTOs with common functionality.

```python
from archipy.models.dtos.base_dtos import BaseDTO
from pydantic import BaseModel

class UserDTO(BaseDTO):
    id: str
    username: str
    email: str
    created_at: datetime
```

::: archipy.models.dtos.base_dtos
    options:
      show_root_heading: true
      show_source: true

### Email DTOs

DTOs for email-related operations.

```python
from archipy.models.dtos.email_dtos import EmailAttachmentDTO

attachment = EmailAttachmentDTO(
    filename="document.pdf",
    content_type="application/pdf",
    content=b"..."
)
```

::: archipy.models.dtos.email_dtos
    options:
      show_root_heading: true
      show_source: true

### Error DTOs

Standardized error response format.

```python
from archipy.models.dtos.error_dto import ErrorDetailDTO

error = ErrorDetailDTO(
    code="USER_NOT_FOUND",
    message="User not found",
    details={"user_id": "123"}
)
```

::: archipy.models.dtos.error_dto
    options:
      show_root_heading: true
      show_source: true

### Pagination DTO

Handles pagination parameters for queries.

```python
from archipy.models.dtos.pagination_dto import PaginationDTO

pagination = PaginationDTO(
    page=1,
    page_size=10,
    total_items=100
)
```

::: archipy.models.dtos.pagination_dto
    options:
      show_root_heading: true
      show_source: true

### Range DTOs

Handles range-based queries and filters.

```python
from archipy.models.dtos.range_dtos import (
    RangeDTO,
    IntegerRangeDTO,
    DateRangeDTO,
    DatetimeRangeDTO
)

# Integer range
int_range = IntegerRangeDTO(start=1, end=100)

# Date range
date_range = DateRangeDTO(
    start=date(2023, 1, 1),
    end=date(2023, 12, 31)
)

# Datetime range
dt_range = DatetimeRangeDTO(
    start=datetime(2023, 1, 1),
    end=datetime(2023, 12, 31)
)
```

::: archipy.models.dtos.range_dtos
    options:
      show_root_heading: true
      show_source: true

### Search Input DTO

Standardized search parameters.

```python
from archipy.models.dtos.search_input_dto import SearchInputDTO

search = SearchInputDTO[str](
    query="john",
    filters={"active": True},
    pagination=pagination
)
```

::: archipy.models.dtos.search_input_dto
    options:
      show_root_heading: true
      show_source: true

### Sort DTO

Handles sorting parameters for queries.

```python
from archipy.models.dtos.sort_dto import SortDTO

sort = SortDTO[str](
    field="created_at",
    order="desc"
)
```

::: archipy.models.dtos.sort_dto
    options:
      show_root_heading: true
      show_source: true

## Entities

### SQLAlchemy Base Entities

Base classes for SQLAlchemy entities with various mixins for different capabilities.

```python
from archipy.models.entities.sqlalchemy.base_entities import (
    BaseEntity,
    UpdatableEntity,
    DeletableEntity,
    AdminEntity,
    ManagerEntity,
    UpdatableDeletableEntity,
    ArchivableEntity,
    UpdatableAdminEntity,
    UpdatableManagerEntity,
    ArchivableDeletableEntity,
    UpdatableDeletableAdminEntity,
    UpdatableDeletableManagerEntity,
    ArchivableAdminEntity,
    ArchivableManagerEntity,
    UpdatableManagerAdminEntity,
    ArchivableManagerAdminEntity,
    ArchivableDeletableAdminEntity,
    ArchivableDeletableManagerEntity,
    UpdatableDeletableManagerAdminEntity,
    ArchivableDeletableManagerAdminEntity
)
from sqlalchemy import Column, String

# Basic entity
class User(BaseEntity):
    __tablename__ = "users"
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)

# Entity with update tracking
class Post(UpdatableEntity):
    __tablename__ = "posts"
    title = Column(String(200))
    content = Column(String)

# Entity with soft deletion
class Comment(DeletableEntity):
    __tablename__ = "comments"
    text = Column(String)

# Entity with admin tracking
class AdminLog(AdminEntity):
    __tablename__ = "admin_logs"
    action = Column(String)

# Entity with manager tracking
class ManagerLog(ManagerEntity):
    __tablename__ = "manager_logs"
    action = Column(String)
```

::: archipy.models.entities.sqlalchemy.base_entities
    options:
      show_root_heading: true
      show_source: true

## Errors

### Custom Errors

Application-specific error classes.

```python
from archipy.models.errors.custom_errors import (
    BaseError,
    InvalidTokenError,
    InvalidEntityTypeError
)

class UserNotFoundError(BaseError):
    def __init__(self, user_id: str):
        super().__init__(
            code="USER_NOT_FOUND",
            message=f"User with ID {user_id} not found"
        )
```

::: archipy.models.errors.custom_errors
    options:
      show_root_heading: true
      show_source: true

## Types

### Base Types

Basic type definitions used throughout the application.

::: archipy.models.types.base_types
    options:
      show_root_heading: true
      show_source: true

### Email Types

Type definitions for email-related operations.

::: archipy.models.types.email_types
    options:
      show_root_heading: true
      show_source: true

### Error Message Types

Standardized error message types for consistent error handling.

::: archipy.models.types.error_message_types
    options:
      show_root_heading: true
      show_source: true

### Language Type

Language code type definition.

::: archipy.models.types.language_type
    options:
      show_root_heading: true
      show_source: true

### Sort Order Type

Sort order type definition for queries.

::: archipy.models.types.sort_order_type
    options:
      show_root_heading: true
      show_source: true

## Key Classes

### BaseDTO

Class: `archipy.models.dtos.base_dtos.BaseDTO`

Base class for all DTOs with features:
- Pydantic model inheritance
- JSON serialization
- Validation
- Type hints
- Common utility methods

### BaseEntity

Class: `archipy.models.entities.sqlalchemy.base_entities.BaseEntity`

Base class for SQLAlchemy entities with features:
- UUID primary key
- Timestamp fields (created_at, updated_at)
- Common query methods
- Relationship support
- Type-safe column definitions
- Mixin support for:
  - Update tracking
  - Soft deletion
  - Admin tracking
  - Manager tracking
  - Archiving
  - Combined capabilities

### BaseError

Class: `archipy.models.errors.custom_errors.BaseError`

Base class for custom errors with features:
- Standardized error format
- Error code system
- Detailed error messages
- Stack trace support
- Error context
- Common error types:
  - InvalidTokenError
  - InvalidEntityTypeError
