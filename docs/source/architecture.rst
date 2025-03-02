.. _architecture:

Architecture
===========

Design Philosophy
----------------

ArchiPy is designed to standardize and simplify Python application development by providing a flexible set of building blocks that work across different architectural approaches. Rather than enforcing a single architectural pattern, ArchiPy offers components that can be applied to:

* Layered Architecture
* Hexagonal Architecture (Ports & Adapters)
* Clean Architecture
* Domain-Driven Design
* Service-Oriented Architecture
* And more...

These building blocks help maintain consistency, testability, and maintainability regardless of the specific architectural style chosen for your project.

.. image:: ../assets/architecture_overview.png
   :alt: ArchiPy Architecture Overview
   :align: center
   :width: 600px

Core Building Blocks
------------------

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~

ArchiPy provides a standardized way to manage configuration across your application:

.. code-block:: python

    from archipy.configs.base_config import BaseConfig

    class AppConfig(BaseConfig):
        DATABASE = {
            "HOST": "localhost",
            "PORT": 5432,
            "USERNAME": "user",
            "PASSWORD": "password"
        }

        DEBUG = True

    # Set global configuration
    config = AppConfig()
    BaseConfig.set_global(config)

Adapters & Ports
~~~~~~~~~~~~~~

ArchiPy implements the ports and adapters pattern to isolate the application core from external dependencies:

.. code-block:: python

    # Port: defines an interface (contract)
    from typing import Protocol

    class UserRepositoryPort(Protocol):
        def get_by_id(self, user_id: str) -> User: ...
        def create(self, user: User) -> User: ...

    # Adapter: implements the interface for a specific technology
    class SqlAlchemyUserRepository:
        def __init__(self, db_adapter: SqlAlchemyAdapter):
            self.db_adapter = db_adapter

        def get_by_id(self, user_id: str) -> User:
            return self.db_adapter.get_by_uuid(User, user_id)

        def create(self, user: User) -> User:
            return self.db_adapter.create(user)

    # Application core uses the port, not the adapter
    class UserService:
        def __init__(self, repository: UserRepositoryPort):
            self.repository = repository

        def get_user(self, user_id: str) -> User:
            return self.repository.get_by_id(user_id)

Entity Models
~~~~~~~~~~~

Standardized entity models provide a consistent approach to domain modeling:

.. code-block:: python

    from sqlalchemy import Column, String
    from archipy.models.entities import BaseEntity

    class User(BaseEntity):
        __tablename__ = "users"

        name = Column(String(100))
        email = Column(String(255), unique=True)

Data Transfer Objects (DTOs)
~~~~~~~~~~~~~~~~~~~~~~~~~

Define consistent data structures for transferring data between layers:

.. code-block:: python

    from pydantic import BaseModel, EmailStr
    from archipy.models.dtos import BaseDTO

    class UserCreateDTO(BaseDTO):
        name: str
        email: EmailStr

    class UserResponseDTO(BaseDTO):
        id: str
        name: str
        email: EmailStr
        created_at: datetime

Example Architectures
--------------------

Layered Architecture
~~~~~~~~~~~~~~~~~

ArchiPy can be used with a traditional layered architecture approach:

.. code-block:: text

    ┌───────────────────────┐
    │     Presentation      │  API, UI, CLI
    ├───────────────────────┤
    │     Application       │  Services, Workflows
    ├───────────────────────┤
    │       Domain          │  Business Logic, Entities
    ├───────────────────────┤
    │    Infrastructure     │  Adapters, Repositories, External Services
    └───────────────────────┘

Clean Architecture
~~~~~~~~~~~~~~~

ArchiPy supports Clean Architecture principles:

.. code-block:: text

    ┌─────────────────────────────────────────────┐
    │                  Entities                    │
    │     Domain models, business rules            │
    ├─────────────────────────────────────────────┤
    │                  Use Cases                   │
    │     Application services, business workflows │
    ├─────────────────────────────────────────────┤
    │                 Interfaces                   │
    │     Controllers, presenters, gateways        │
    ├─────────────────────────────────────────────┤
    │                Frameworks                    │
    │     External libraries, UI, DB, devices      │
    └─────────────────────────────────────────────┘

Hexagonal Architecture
~~~~~~~~~~~~~~~~~~

For projects using a Hexagonal (Ports & Adapters) approach:

.. code-block:: text

    ┌───────────────────────────────────────────────────┐
    │                                                   │
    │                 Application Core                  │
    │                                                   │
    │  ┌─────────────────────────────────────────────┐  │
    │  │                                             │  │
    │  │           Domain Logic / Models             │  │
    │  │                                             │  │
    │  └─────────────────────────────────────────────┘  │
    │                                                   │
    │  ┌─────────────┐         ┌─────────────────────┐  │
    │  │             │         │                     │  │
    │  │  Input      │         │  Output Ports       │  │
    │  │  Ports      │         │                     │  │
    │  │             │         │                     │  │
    │  └─────────────┘         └─────────────────────┘  │
    │                                                   │
    └───────────────────────────────────────────────────┘
            ▲                           ▲
            │                           │
            │                           │
    ┌───────┴──────────┐      ┌────────┴────────────┐
    │                  │      │                     │
    │  Input Adapters  │      │  Output Adapters    │
    │  (Controllers)   │      │  (Repositories,     │
    │                  │      │   Clients, etc.)    │
    │                  │      │                     │
    └──────────────────┘      └─────────────────────┘

Practical Implementation
---------------------

Let's see how a complete application might be structured using ArchiPy:

.. code-block:: text

    my_app/
    ├── configs/
    │   └── app_config.py          # Application configuration
    ├── adapters/
    │   ├── db/                    # Database adapters
    │   └── api/                   # API adapters
    ├── core/
    │   ├── models/                # Domain models
    │   ├── ports/                 # Interface definitions
    │   └── services/              # Business logic
    ├── repositories/              # Data access
    ├── api/                       # API routes
    └── main.py                    # Application entry point

Code Example
-----------

Here's how you might structure a FastAPI application using ArchiPy:

.. code-block:: python

    # adapters/db/user_repository.py
    from archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters import SqlAlchemyAdapter
    from core.models.user import User

    class UserRepository:
        def __init__(self, db_adapter: SqlAlchemyAdapter):
            self.db_adapter = db_adapter

        def get_user_by_id(self, user_id: str) -> User:
            return self.db_adapter.get_by_uuid(User, user_id)

        def create_user(self, user: User) -> User:
            return self.db_adapter.create(user)

    # core/services/user_service.py
    from core.models.user import User
    from adapters.db.user_repository import UserRepository

    class UserService:
        def __init__(self, user_repository: UserRepository):
            self.user_repository = user_repository

        def register_user(self, name: str, email: str) -> User:
            # Business logic and validation here
            user = User(name=name, email=email)
            return self.user_repository.create_user(user)

    # api/users.py
    from fastapi import APIRouter, Depends
    from core.services.user_service import UserService
    from archipy.models.dtos import BaseDTO

    router = APIRouter()

    class UserCreateDTO(BaseDTO):
        name: str
        email: str

    @router.post("/users/")
    def create_user(
        data: UserCreateDTO,
        user_service: UserService = Depends(get_user_service)
    ):
        user = user_service.register_user(data.name, data.email)
        return {"id": str(user.test_uuid), "name": user.name, "email": user.email}

    # main.py
    from fastapi import FastAPI
    from archipy.helpers.utils.app_utils import AppUtils
    from archipy.configs.base_config import BaseConfig

    app = AppUtils.create_fastapi_app(BaseConfig.global_config())
    app.include_router(users_router)

By providing standardized building blocks rather than enforcing a specific architecture, ArchiPy helps teams maintain consistent development practices while allowing flexibility to choose the architectural pattern that best fits their needs.
