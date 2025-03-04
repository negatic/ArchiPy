# Decorator Examples

This page demonstrates how to use ArchiPy's decorators.

## Basic Usage

```python
from archipy.helpers.decorators.timing import timing_decorator
from archipy.helpers.decorators.retry import retry


# Measure function execution time
@timing_decorator
def my_function():
    # Function code
    pass


# Retry function on failure
@retry(max_attempts=3, delay=1)
def external_api_call():
    # Function that might fail
    pass
```

This documentation is being migrated from Sphinx to MkDocs format.
Please check back soon for complete content.
