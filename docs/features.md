# Features

ArchiPy provides a robust framework for structured Python development, focusing on standardization, testability, and productivity.

## Configuration Management

- **Standardized Configs**: Use `base_config` and `config_template` for consistent setup.
- **Injection**: Seamlessly inject configurations into components.

## Adapters & Mocks

- **Common Adapters**: Pre-built for Redis, SQLAlchemy, and email.
- **Mocks**: Testable mocks (e.g., `redis_mocks`, `sqlalchemy_mocks`) for isolated testing.
- **Async Support**: Synchronous and asynchronous implementations.

## Data Standardization

- **Base Entities**: Standardized SQLAlchemy entities (`base_entities.py`).
- **DTOs**: Pydantic-based DTOs (e.g., `pagination_dto`, `error_dto`).
- **Type Safety**: Enforced via `pydantic` and `mypy`.

## Helper Utilities

- **Utilities**: Tools like `datetime_utils`, `jwt_utils`, `password_utils`, and `totp_utils`.
- **Decorators**: `retry`, `singleton`, `sqlalchemy_atomic`, etc.
- **Interceptors**: Rate limiting (FastAPI), tracing (gRPC).
- **Enhanced Security**: Cryptographically secure implementations with `secrets` module.
- **Type Safety**: Consistent type checking and casting for robust interfaces.

## BDD Testing

- **Behave Integration**: Pre-configured for sync/async scenarios.
- **Feature Files**: Examples like `app_utils.feature`, `totp_utils.feature`.
- **Step Definitions**: Comprehensive steps for testing (e.g., `jwt_utils_steps.py`).

## Best Practices & Tooling

- **Poetry**: Dependency management for reproducible builds.
- **Pre-commit**: Automated checks with `ruff`, `black`, and `mypy`.
- **Structure**: Clean architecture with `pyproject.toml` for modern Python development.

## Modular Design

- **Optional Dependencies**: Install only what you need (e.g., `archipy[redis]`).
- **Extensible**: Add custom adapters and helpers easily.
