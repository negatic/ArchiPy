# Configs

## Overview

The configs module provides tools for standardized configuration management and injection, supporting consistent setup across services like databases, Redis, and email.

## Installation

This module is included in the base ArchiPy installation:

```bash
# Add ArchiPy to your project
poetry add archipy
```

## Source Code

📁 Location: `archipy/configs/`

🔗 [Browse Source](https://github.com/SyntaxArc/ArchiPy/tree/master/archipy/configs)

## API Stability

| Component | Status | Notes |
|-----------|---------|-------|
| BaseConfig | 🟢 Stable | Production-ready |
| Config Templates | 🟢 Stable | Production-ready |
| Environment Types | 🟢 Stable | Production-ready |

## Examples

For practical examples, see the [Configuration Management Guide](../examples/config_management.md).

## Configuration Classes

### Base Config

Documentation for `archipy.configs.base_config` module.

```python
from archipy.configs.base_config import BaseConfig

class AppConfig(BaseConfig):
    APP_NAME: str = "MyService"
    DEBUG: bool = False

    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
```

*Includes all members, undocumented members, and shows inheritance.*

### Config Templates

Documentation for `archipy.configs.config_template` module.

```python
from archipy.configs.config_template import SqlAlchemyConfig

class DatabaseConfig(SqlAlchemyConfig):
    DB_POOL_SIZE: int = 5
    DB_POOL_TIMEOUT: int = 30
```

*Includes all members, undocumented members, and shows inheritance.*

## Key Classes

### BaseConfig

Class: `archipy.configs.base_config.BaseConfig`

Configures:

- Environment variable support
- Type validation
- Global configuration access
- Nested configuration support

*Includes all members, undocumented members, and shows inheritance.*

### SqlAlchemyConfig

Class: `archipy.configs.config_template.SqlAlchemyConfig`

Configures:

- Database connection settings
- Pool configuration
- Migration settings
- Debug options

*Includes all members, undocumented members, and shows inheritance.*

### RedisConfig

Class: `archipy.configs.config_template.RedisConfig`

Configures:

- Connection settings
- Pool configuration
- SSL options
- Sentinel support

*Includes all members, undocumented members, and shows inheritance.*

### EmailConfig

Class: `archipy.configs.config_template.EmailConfig`

Configures:

- SMTP settings
- Authentication
- TLS options
- Default headers

*Includes all members, undocumented members, and shows inheritance.*

### FastAPIConfig

Class: `archipy.configs.config_template.FastAPIConfig`

Configures:

- API versioning
- CORS configuration
- Rate limiting
- Documentation

*Includes all members, undocumented members, and shows inheritance.*

### GrpcConfig

Class: `archipy.configs.config_template.GrpcConfig`

Configures:

- Server settings
- Client configuration
- Interceptors
- SSL/TLS options

*Includes all members, undocumented members, and shows inheritance.*

### SentryConfig

Class: `archipy.configs.config_template.SentryConfig`

Configures:

- DSN configuration
- Environment settings
- Sample rates
- Performance monitoring

*Includes all members, undocumented members, and shows inheritance.*

### ElasticSearchConfig

Class: `archipy.configs.config_template.ElasticSearchConfig`

Configures:

- Cluster configuration
- Authentication
- Index settings
- Retry policies

*Includes all members, undocumented members, and shows inheritance.*

### ElasticSearchAPMConfig

Class: `archipy.configs.config_template.ElasticSearchAPMConfig`

Configures:

- APM server settings
- Service name
- Transaction sampling
- Instrumentation

*Includes all members, undocumented members, and shows inheritance.*

### KafkaConfig

Class: `archipy.configs.config_template.KafkaConfig`

Configures:

- Broker configuration
- Consumer groups
- Producer settings
- Security options

*Includes all members, undocumented members, and shows inheritance.*

### EnvironmentType

Class: `archipy.configs.environment_type.EnvironmentType`

Configures:

- Environment types (DEV, STAGING, PROD)
- Environment-specific behaviors
- Configuration validation rules

*Includes all members, undocumented members, and shows inheritance.*
