# Welcome to ArchiPy

![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)

<div style="float: right; margin-left: 20px;">
    <img src="assets/logo.jpg" alt="ArchiPy Logo" width="150"/>
</div>

**Architecture + Python – Structured Development Simplified**

ArchiPy provides a clean architecture framework for Python applications that:

* Standardizes configuration management
* Offers pluggable adapters with testing mocks
* Enforces consistent data models
* Promotes maintainable code organization
* Simplifies testing with BDD support

## Quick Start

```bash
# Install using pip
pip install archipy

# Or with poetry
poetry add archipy
```

## Key Features

ArchiPy is a comprehensive framework designed to streamline Python application development through clean architecture principles:

- **Modular Adapters**: Plug-and-play implementations with ready-to-use mocks for databases, Redis, email, and more
- **Robust Configuration**: Type-safe configuration management with environment variable support
- **Standardized Models**: Consistent data modeling with DTOs, entities, and well-defined types
- **Development Helpers**: Decorators, metaclasses, and utilities to accelerate development
- **BDD Testing**: Integrated Behave support for behavior-driven development

## Project Structure

```
archipy/
│
├── adapters/          # Interfaces to external systems 
├── configs/           # Configuration management
├── helpers/           # Development utilities
│   ├── decorators/    # Function/method decorators
│   ├── interceptors/  # Communication interceptors
│   ├── metaclasses/   # Class creators and modifiers
│   └── utils/         # General-purpose utilities
└── models/            # Domain objects
    ├── dtos/          # Data Transfer Objects
    ├── entities/      # Business entities
    ├── errors/        # Error definitions
    └── types/         # Type definitions
```