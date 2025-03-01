<img src="./assets/logo.jpg" alt="ArchiPy Logo" width="150"/>

# ArchiPy - Architecture + Python

[![Forks](https://img.shields.io/github/forks/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/network/members)
[![Stars](https://img.shields.io/github/stars/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/stargazers)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Documentation](https://readthedocs.org/projects/archipy/badge/?version=latest)](https://archipy.readthedocs.io/)
[![License](https://img.shields.io/github/license/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/blob/master/LICENSE)
[![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen)](https://github.com/SyntaxArc/ArchiPy)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](https://github.com/SyntaxArc/ArchiPy/blob/master/CONTRIBUTING.md)
[![PyPI - Version](https://img.shields.io/pypi/v/archipy)](https://pypi.org/project/archipy/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/archipy)](https://pypi.org/project/archipy/)
[![Contributors](https://img.shields.io/github/contributors/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/commits/main)
[![Open Issues](https://img.shields.io/github/issues/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/issues?q=is%3Aissue+is%3Aclosed)
[![Pull Requests](https://img.shields.io/github/issues-pr/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/pulls)
[![Repo Size](https://img.shields.io/github/repo-size/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy)
[![Code Size](https://img.shields.io/github/languages/code-size/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy)

## **Structured Python Development Made Simple**

ArchiPy is a Python framework designed to provide a standardized, scalable, and maintainable architecture for modern applications. Built with Python 3.13+, it offers a suite of tools, utilities, and best practices to streamline configuration management, testing, and development workflows while adhering to clean architecture principles.

---

## 📋 Table of Contents

- [Goals](#-goals)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Development](#-development)
- [Contributing](#-contributing)
- [Code of Conduct](#-code-of-conduct)
- [License](#-license)
- [Contact](#-contact)
- [Links](#-links)

---

## 🎯 Goals

ArchiPy is built with the following objectives in mind:

1. **Configuration Management & Injection**
   Simplify and standardize configuration handling with tools like `base_config.py` and dependency injection, ensuring consistent and reusable setups across projects.

2. **Common Adapters & Mocks**
   Provide ready-to-use adapters (e.g., Redis, SQLAlchemy, email) with corresponding mocks for seamless delegation and testing without external dependencies.

3. **Standardized Entities & DTOs**
   Offer base entities, data transfer objects (DTOs), and type definitions to enforce consistency and reduce boilerplate in data modeling.

4. **Common Helpers for Everyday Tasks**
   Include a rich set of utilities, decorators (e.g., retry, singleton), and interceptors (e.g., FastAPI rate limiting, gRPC tracing) to simplify routine development work.

5. **Behavior-Driven Development (BDD) Support**
   Integrate `behave` with pre-configured examples for synchronous and asynchronous scenario testing, enabling robust feature validation.

6. **Best Practices & Development Structure**
   Leverage `poetry`, `pre-commit`, `pyproject.toml`, and tools like `ruff` and `black` to enforce coding standards and provide an optimal Python development structure.

---

## ✨ Features

- **Config Standardization**: Tools for managing and injecting configurations effortlessly (`base_config`, `config_template`).
- **Adapters & Mocks**: Pre-built adapters for Redis, SQLAlchemy, and email, with mocks like `redis_mocks` and `sqlalchemy_mocks` for testing.
- **Data Standardization**: Base entities (`base_entities.py`), DTOs (e.g., `pagination_dto`, `error_dto`), and type safety with `pydantic` and `mypy`.
- **Helper Utilities**: A collection of reusable tools including `datetime_utils`, `jwt_utils`, `password_utils`, and decorators like `sqlalchemy_atomic` and `timing_decorator`.
- **BDD Testing**: Fully integrated `behave` setup with feature files (e.g., `app_utils.feature`) and step definitions for sync/async testing.
- **Modern Tooling**: Dependency management with `poetry`, code quality with `ruff` and `black`, and pre-commit hooks for automated checks.
- **Modular Design**: Optional dependencies for Redis, FastAPI, gRPC, PostgreSQL, and more, installable via `archipy[feature]`.

---

## 🛠️ Prerequisites

Before using ArchiPy, ensure you have:

- **Python 3.13 or higher**
  Check your version with:
  ```bash
  python --version
  ```
  [Download Python 3.13+](https://www.python.org/downloads/) if needed.

- **Poetry**
  Install Poetry for dependency management: [Poetry Installation Guide](https://python-poetry.org/docs/).

---

## 🚀 Installation

### From PyPI

Install ArchiPy easily with `pip` or `poetry`:

```bash
# Basic installation
pip install archipy

# With optional dependencies (e.g., Redis and FastAPI)
pip install archipy[redis,fastapi]
```

Using Poetry:
```bash
poetry add archipy

# With optional dependencies
poetry add archipy[redis,fastapi]
```

### From Source

For development or cutting-edge features:
1. Clone the repository:
   ```bash
   git clone https://github.com/SyntaxArc/ArchiPy.git
   cd ArchiPy
   ```
2. Set up the project:
   ```bash
   make setup
   ```
3. Install dependencies:
   ```bash
   make install
   ```

---

## 🎯 Usage

### Optional Dependencies

ArchiPy’s modular design lets you install only what you need:

| Feature              | Installation Command            | Description                                      |
|----------------------|---------------------------------|--------------------------------------------------|
| Redis                | `archipy[redis]`                | Redis client for caching and data storage        |
| Elastic APM          | `archipy[elastic-apm]`          | Application performance monitoring with Elastic  |
| FastAPI              | `archipy[fastapi]`              | FastAPI framework for building APIs              |
| JWT                  | `archipy[jwt]`                  | JSON Web Token support for authentication        |
| Kavenegar            | `archipy[kavenegar]`            | SMS service integration via Kavenegar            |
| Prometheus           | `archipy[prometheus]`           | Metrics and monitoring with Prometheus           |
| Sentry               | `archipy[sentry]`               | Error tracking with Sentry                       |
| Dependency Injection | `archipy[dependency-injection]` | Dependency injection framework                   |
| Scheduler            | `archipy[scheduler]`            | Task scheduling with APScheduler                 |
| gRPC                 | `archipy[grpc]`                 | gRPC support for high-performance RPC            |
| PostgreSQL           | `archipy[postgres]`             | PostgreSQL database support with SQLAlchemy      |
| aiosqlite            | `archipy[aiosqlite]`            | Asynchronous SQLite database support             |
| FakeRedis            | `archipy[fakeredis]`            | Mock Redis client for testing without a server   |

---

## 🛠️ Development

### Common Commands

Run `make help` for all commands. Key ones include:
- **Format Code**: `make format`
- **Run Tests**: `make behave`
- **Lint Code**: `make lint`
- **Build Project**: `make build`
- **Update Dependencies**: `make update`

### Versioning

We follow [Semantic Versioning (SemVer)](https://semver.org/) principles:

- **Bump Patch Version** (Bug fixes): `make bump-patch`
- **Bump Minor Version** (New features): `make bump-minor`
- **Bump Major Version** (Breaking changes): `make bump-major`

Add a custom message to your version bump:
```bash
make bump-patch message="Your custom message"
```

For more detailed information about development processes, refer to our [contribution guidelines](CONTRIBUTING.md).

---

## 🤝 Contributing

Contributions are welcome! See our [contribution guidelines](CONTRIBUTING.md) for details on setup, workflow, and standards.

---

## 📜 Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment for all contributors and users. Please review it before participating.

---

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---

## 📞 Contact

For questions or feedback, feel free to reach out:

- **Mehdi Einali**: [einali@gmail.com](mailto:einali@gmail.com)
- **Hossein Nejati**: [hosseinnejati14@gmail.com](mailto:hosseinnejati14@gmail.com)

---

## 🔗 Links

- [GitHub](https://github.com/SyntaxArc/ArchiPy)
- [Documentation](https://archipy.readthedocs.io/)
- [Issues](https://github.com/SyntaxArc/ArchiPy/issues)
- [Contributing](https://github.com/SyntaxArc/ArchiPy/blob/master/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/SyntaxArc/ArchiPy/blob/master/CODE_OF_CONDUCT.md)
