# API Reference

Welcome to the ArchiPy API reference documentation. This section provides detailed information about all modules, classes, and functions in ArchiPy.

## Core Modules

### Adapters

The adapters module provides standardized interfaces to external systems:

- [Adapters Documentation](adapters.md)
- [ORM Adapters](adapters.md#orm)
- [Redis Adapters](adapters.md#redis)
- [Email Adapters](adapters.md#email)

### Configs

Configuration management and injection tools:

- [Configs Documentation](configs.md)
- [Base Config](configs.md#base-config)
- [Config Templates](configs.md#config-templates)

### Helpers

Utility functions and support classes:

- [Helpers Documentation](helpers.md)
- [Decorators](../examples/helpers/decorators.md)
- [Utils](../examples/helpers/utils.md)
- [Metaclasses](../examples/helpers/metaclasses.md)
- [Interceptors](../examples/helpers/interceptors.md)

### Models

Core data structures and types:

- [Models Documentation](models.md)
- [Entities](models.md#entities)
- [Data Transfer Objects](models.md#data-transfer-objects-dtos)
- [Errors](models.md#errors)
- [Types](models.md#types)

## Source Code Organization

The ArchiPy source code is organized into the following structure:

```
archipy/
├── adapters/           # External system integrations
│   ├── email/         # Email service adapters
│   ├── orm/           # Database ORM adapters
│   └── redis/         # Redis adapters
├── configs/           # Configuration management
│   ├── base_config.py
│   └── templates/
├── helpers/           # Utility functions
│   ├── decorators/
│   ├── interceptors/
│   ├── metaclasses/
│   └── utils/
└── models/            # Core data structures
    ├── dtos/
    ├── entities/
    ├── errors/
    └── types/
```

## API Stability

ArchiPy follows semantic versioning and marks API stability as follows:

- 🟢 **Stable**: Production-ready APIs, covered by semantic versioning
- 🟡 **Beta**: APIs that are stabilizing but may have breaking changes
- 🔴 **Alpha**: Experimental APIs that may change significantly

See the [Changelog](../changelog.md) for version history and breaking changes.

## Contributing

For information about contributing to ArchiPy's development, please see:

- [Contributing Guide](../contributing.md)
- [Development Guide](../development.md)
- [Documentation Guide](../contributing-docs.md)
