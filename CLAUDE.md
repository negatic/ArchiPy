# ArchiPy Development Guide

## Commands
- **Setup**: `poetry install --with dev --all-extras`
- **Format**: `make format` (Black, 120 char line length)
- **Lint**: `make lint` (Ruff + MyPy)
- **Test**: `make behave` (all tests)
- **Single test**: `poetry run behave features/file_name.feature`
- **Specific scenario**: `poetry run behave features/file_name.feature:line_number`
- **All checks**: `make check` (lint + test)
- **Pre-commit hooks**: `make pre-commit`

## Code Style
- **Imports**: Use strict section order: `future → stdlib → third-party → first-party → local`
- **Typing**: Strict typing required with MyPy (`disallow_untyped_defs=true`)
- **Quotes**: Double quotes for inline strings, single quotes for multiline
- **Docstrings**: Google-style docstrings required for all public APIs
- **Naming**: Snake case for functions/vars, PascalCase for classes (enforced by Ruff)
- **Error handling**: Use specific exception types, add to custom_errors.py when needed
- **Line length**: 120 characters maximum
- **Complexity**: Keep McCabe complexity below 10
- **Formatting**: Files end with newline, consistent indent (4 spaces)
