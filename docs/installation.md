# Installation

## Prerequisites

Before starting, ensure you have:

- **Python 3.13 or higher**

    ArchiPy requires Python 3.13+. Check your version with:

    ```bash
    python --version
    ```

    If needed, [download Python 3.13+](https://www.python.org/downloads/).

- **Poetry** (for dependency management)

    Poetry manages dependencies and project setup. Install it via the [official guide](https://python-poetry.org/docs/).

## Installation Methods

### Using pip

Install the core library:

```bash
pip install archipy
```

With optional dependencies (e.g., Redis, FastAPI):

```bash
pip install archipy[redis,fastapi]
```

### Using Poetry

Add the core library:

```bash
poetry add archipy
```

With optional dependencies:

```bash
poetry add "archipy[redis,fastapi]"
```

## Optional Dependencies

ArchiPy supports modular features:

| Feature | Installation Command |
| ------- | -------------------- |
| Redis | `archipy[redis]` |
| FastAPI | `archipy[fastapi]` |
| JWT | `archipy[jwt]` |
| Kavenegar | `archipy[kavenegar]` |
| Prometheus | `archipy[prometheus]` |
| Sentry | `archipy[sentry]` |
| Dependency Injection | `archipy[dependency-injection]` |
| Scheduler | `archipy[scheduler]` |
| gRPC | `archipy[grpc]` |
| PostgreSQL | `archipy[postgres]` |
| FakeRedis | `archipy[fakeredis]` |
| Full list | See [Usage](usage.md) section |

## Development Installation

For contributors:

```bash
# Clone the repository
git clone https://github.com/SyntaxArc/ArchiPy.git
cd ArchiPy

# Set up the project
make setup

# Install dependencies
make install

# Optional: Install dev tools
make install-dev
```

## Troubleshooting

If issues arise, verify:

1. Python version is 3.13+
2. `pip` or `poetry` is updated (e.g., `pip install --upgrade pip`)
3. Build tools (`setuptools`, `wheel`) are installed

!!! tip "IDE Integration"
    For the best development experience, use an IDE that supports Python type hints, such as PyCharm or VS Code with the Python extension.
