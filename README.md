# ArchiPy <img src="/assets/logo.jpg" width="30" height="30" alt="Archipy Logo">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![PyPI - Version](https://img.shields.io/pypi/v/archipy)](https://pypi.org/project/archipy/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/archipy)](https://pypi.org/project/archipy/)
[![Documentation](https://readthedocs.org/projects/archipy/badge/?version=latest)](https://archipy.readthedocs.io/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![License](https://img.shields.io/github/license/SyntaxArc/ArchiPy)](https://github.com/SyntaxArc/ArchiPy/blob/master/LICENSE)

[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linter-ruff-red)](https://github.com/charliermarsh/ruff)
[![Mypy](https://img.shields.io/badge/type%20checker-mypy-blue)](https://github.com/python/mypy)
[![Behave](https://img.shields.io/badge/tested%20with-behave-brightgreen)](https://github.com/behave/behave)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/SyntaxArc/ArchiPy/actions)

[![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen)](https://github.com/SyntaxArc/ArchiPy)
[![GitHub issues](https://img.shields.io/badge/issues-open-orange)](https://github.com/SyntaxArc/ArchiPy/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](https://github.com/SyntaxArc/ArchiPy/blob/master/CONTRIBUTING.md)

**Architecture + Python – Perfect for Structured Design**

ArchiPy is a Python project designed to provide a robust and structured architecture for building scalable and
maintainable applications. It integrates modern Python tools and libraries to streamline development, testing, and
deployment.

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Links](#-links)

---

## ✨ Features

- **Modern Python Stack**: Built with Python 3.13 and leveraging tools like `pydantic`, `fastapi`, `gRPC` and
  `sqlalchemy`.
- **Modular Design**: Optional dependencies for Redis, gRPC, PostgreSQL, Prometheus, and more.
- **Type Safety**: Enforced by `mypy` and `pydantic` for robust code.
- **Testing**: Integrated with `pytest` and `behave` for comprehensive testing.
- **Linting and Formatting**: Uses `ruff` and `black` for clean and consistent code.
- **Pre-commit Hooks**: Automates code quality checks before commits.
- **Dependency Management**: Managed by `poetry` for reproducible builds.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13 or higher**
  `archipy` is compatible with Python 3.13 and above but does not support Python 4 or higher.
  To check your Python version, run:
  ```bash
  python --version
  ```
  If your Python version is lower than 3.13, [download and install the latest version of Python](https://www.python.org/downloads/).

- **Poetry** (for dependency management)
  Poetry is required to manage dependencies and install the project. If you don't have Poetry installed, follow the [official installation guide](https://python-poetry.org/docs/).

---

## 🚀 Installation

### From PyPI

The simplest way to install ArchiPy is from PyPI:

```bash
# Basic installation
pip install archipy

# With optional dependencies
pip install archipy[redis,fastapi]
```

Or using Poetry:

```bash
# Basic installation
poetry add archipy

# With optional dependencies
poetry add archipy[redis,fastapi]
```

### From Source

To install from source:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SyntaxArc/ArchiPy.git
   cd ArchiPy
   ```

2. **Set Up the Project**
   ```bash
   make setup
   ```

3. **Install Dependencies**
   ```bash
   make install
   ```

---

## 🎯 Usage

### Optional Dependencies

The library provides optional dependencies for additional functionality. You can install them as needed:

| Feature              | Installation Command            |
|----------------------|---------------------------------|
| Redis                | `archipy[redis]`                |
| Elastic APM          | `archipy[elastic-apm]`          |
| FastAPI              | `archipy[fastapi]`              |
| JWT                  | `archipy[jwt]`                  |
| Kavenegar            | `archipy[kavenegar]`            |
| Prometheus           | `archipy[prometheus]`           |
| Sentry               | `archipy[sentry]`               |
| Dependency Injection | `archipy[dependency-injection]` |
| Scheduler            | `archipy[scheduler]`            |
| gRPC                 | `archipy[grpc]`                 |
| PostgreSQL           | `archipy[postgres]`             |
| aiosqlite            | `archipy[aiosqlite]`            |

### Troubleshooting Installation

If you encounter issues during installation, ensure that:

1. Your Python version is **3.13 or higher**
2. Your package manager (`pip` or `poetry`) is up to date
3. You have the necessary build tools installed (e.g., `setuptools`, `wheel`)

---

## 🛠️ Development

### Common Commands

Run `make help` to see all available commands. Here are some frequently used ones:

- **Format Code** 🧹 `make format`
- **Run Linters** 🔍 `make lint`
- **Run Tests** 🧪 `make behave`
- **Build the Project** 🏗️ `make build`
- **Clean Build Artifacts** 🧽 `make clean`
- **Run All Checks** `make check`
- **Run CI Pipeline Locally** `make ci`
- **Update Dependencies** `make update`

### Version Management

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

We welcome contributions to ArchiPy! Please check out our [contribution guidelines](CONTRIBUTING.md) for details on:

- Setting up your development environment
- Our development workflow
- How to submit effective pull requests
- Code style and quality expectations
- Testing requirements

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

- **GitHub Repository**: [https://github.com/SyntaxArc/ArchiPy](https://github.com/SyntaxArc/ArchiPy)
- **Documentation**: [https://archipy.readthedocs.io/](https://archipy.readthedocs.io/)
- **Bug Tracker**: [https://github.com/SyntaxArc/ArchiPy/issues](https://github.com/SyntaxArc/ArchiPy/issues)

---
