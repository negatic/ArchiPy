# Utilities Examples

This page demonstrates how to use ArchiPy's utility functions.

## Basic Usage

```python
from archipy.helpers.utils.datetime_utils import get_utc_now, format_datetime
from archipy.helpers.utils.string_utils import camel_to_snake, snake_to_camel

# DateTime utilities
now = get_utc_now()
formatted = format_datetime(now, "%Y-%m-%d")

# String utilities
snake_case = camel_to_snake("MyVariableName")  # "my_variable_name"
camel_case = snake_to_camel("my_variable_name")  # "myVariableName"
```

This documentation is being migrated from Sphinx to MkDocs format.
Please check back soon for complete content.