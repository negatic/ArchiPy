# Contributing to ArchiPy 🏗️

First of all, thank you for considering contributing to ArchiPy! This document provides guidelines and instructions for contributing to this project. By following these guidelines, you help maintain the quality and consistency of the codebase.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Installation for Development](#installation-for-development)
  - [Development Commands](#development-commands)
- [Pull Request Process](#pull-request-process)
- [Versioning](#versioning)
- [Getting Help](#getting-help)

## Code of Conduct

This project and everyone participating in it are governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Bug reports help us improve ArchiPy. When creating a bug report, please include as much detail as possible:

1. **Use a clear and descriptive title** for the issue
2. **Describe the exact steps to reproduce the problem**
3. **Provide specific examples** to demonstrate the steps
4. **Describe the behavior you observed and what you expected to see**
5. **Include screenshots or animated GIFs** if possible
6. **Include details about your environment**: Python version, ArchiPy version, operating system, etc.

### Suggesting Enhancements

Suggestions for enhancements help make ArchiPy better for everyone. When suggesting enhancements:

1. **Use a clear and descriptive title**
2. **Provide a step-by-step description of the suggested enhancement**
3. **Explain why this enhancement would be useful to most ArchiPy users**
4. **List any alternatives you've considered**

### Code Contributions

Code contributions are always welcome! Here's how to get started:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write your code and tests
4. Ensure your code passes all tests and linting
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13 or higher**
- **Poetry** (for dependency management)
- **Git**

### Installation for Development

1. Clone your fork of the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ArchiPy.git
   cd ArchiPy
   ```

2. Set up the project environment:
   ```bash
   # Set up project pre-requisites (only needed once)
   make setup

   # Install development dependencies
   make install-dev
   ```

### Development Commands

ArchiPy provides a comprehensive Makefile to simplify development tasks. Here are the most common commands:

#### Environment Management
```bash
# Install core dependencies
make install

# Install development dependencies (including all extras)
make install-dev

# Update dependencies to their latest versions
make update
```

#### Code Quality
```bash
# Format code using black
make format

# Run all linters (ruff, mypy)
make lint

# Run pre-commit hooks on all files
make pre-commit

# Run all checks (linting and tests)
make check
```

#### Testing
```bash
# Run BDD tests with behave
make behave
```

#### Building and Versioning
```bash
# Clean build artifacts
make clean

# Build project distribution
make build

# Display current version
make version

# Bump patch version (for bug fixes)
make bump-patch

# Bump minor version (for new features)
make bump-minor

# Bump major version (for breaking changes)
make bump-major

# Custom version message
make bump-patch message="Your custom message"
```

#### Docker Operations
```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run
```

#### CI Pipeline
```bash
# Run the complete CI pipeline locally
make ci
```

For a complete list of available commands:
```bash
make help
```

## Pull Request Process

1. Ensure your code passes all tests, linting, and type checking (`make check`)
2. Update documentation if needed
3. Include tests for new features or bug fixes
4. The PR should work for Python 3.13 and above
5. All CI checks must pass before merging

Pull requests are usually reviewed within a few days. Maintainers may request changes or ask questions about your implementation.

## Versioning

We follow [Semantic Versioning (SemVer)](https://semver.org/):

- **Patch version** (make bump-patch): Bug fixes and minor improvements
- **Minor version** (make bump-minor): New features, non-breaking changes
- **Major version** (make bump-major): Breaking changes, significant refactoring

Version bumping is handled through the `scripts/bump_version.py` script and can be triggered with the appropriate make commands.

## Getting Help

If you need help with contributing, feel free to:

- Open an issue with your question
- Contact the maintainers directly:
  - Hossein Nejati: [hosseinnejati14@gmail.com](mailto:hosseinnejati14@gmail.com)
  - Mehdi Einali: [einali@gmail.com](mailto:einali@gmail.com)
- Check the project documentation at [https://archipy.readthedocs.io/](https://archipy.readthedocs.io/)

Thank you for contributing to ArchiPy! Your efforts help make this project better for everyone.
