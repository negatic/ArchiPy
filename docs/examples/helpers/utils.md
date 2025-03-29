# Utilities

Examples of ArchiPy's utility functions:

## datetime_utils

Work with dates and times consistently:

```python
from archipy.helpers.utils.datetime_utils import DatetimeUtils

# Get current UTC time
now = DatetimeUtils.get_datetime_utc_now()

# Format for storage/transmission
date_str = DatetimeUtils.get_string_datetime_from_datetime(now)

# Parse date string
parsed = DatetimeUtils.get_datetime_from_string_datetime(date_str)

# Convert to Jalali (Persian) calendar
jalali_date = DatetimeUtils.convert_to_jalali(now)

# Check if date is a holiday in Iran
is_holiday = DatetimeUtils.is_holiday_in_iran(now)
```

## jwt_utils

Generate and verify JWT tokens:

```python
from archipy.helpers.utils.jwt_utils import JWTUtils
from uuid import uuid4

# Generate a user access token
user_id = uuid4()
access_token = JWTUtils.create_access_token(user_id)

# Generate a refresh token
refresh_token = JWTUtils.create_refresh_token(user_id)

# Verify a token
try:
    payload = JWTUtils.verify_access_token(access_token)
    print(f"Token valid for user: {payload['sub']}")
except Exception as e:
    print(f"Invalid token: {e}")
```

## password_utils

Secure password handling:

```python
from archipy.helpers.utils.password_utils import PasswordUtils

# Hash a password
password = "SecureP@ssword123"
hashed = PasswordUtils.hash_password(password)

# Verify password
is_valid = PasswordUtils.verify_password(password, hashed)
print(f"Password valid: {is_valid}")

# Generate a secure password
secure_password = PasswordUtils.generate_password(length=12)
print(f"Generated password: {secure_password}")
```

## file_utils

Handle files securely:

```python
from archipy.helpers.utils.file_utils import FileUtils

# Generate secure link to file
link = FileUtils.generate_secure_file_link("/path/to/document.pdf", expires_in=3600)

# Validate file extension
is_valid = FileUtils.validate_file_extension("document.pdf", ["pdf", "docx", "txt"])
print(f"File is valid: {is_valid}")
```

## base_utils

Validate and sanitize data:

```python
from archipy.helpers.utils.base_utils import BaseUtils

# Sanitize phone number
phone = BaseUtils.sanitize_phone_number("+989123456789")
print(phone)  # 09123456789

# Validate Iranian national code
try:
    BaseUtils.validate_iranian_national_code_pattern("1234567891")
    print("National code is valid")
except Exception as e:
    print(f"Invalid national code: {e}")
```

## error_utils

Standardized exception handling:

```python
from archipy.helpers.utils.error_utils import ErrorUtils
from archipy.models.errors import BaseError
from archipy.models.types.error_message_types import ErrorMessageType

# Create exception detail
detail = ErrorUtils.create_exception_detail(
    ErrorMessageType.INVALID_PHONE,
    lang="en"
)

# Handle exceptions
try:
    # Some code that might fail
    raise ValueError("Something went wrong")
except Exception as e:
    ErrorUtils.capture_exception(e)
```

## app_utils

FastAPI application utilities:

```python
from archipy.helpers.utils.app_utils import AppUtils, FastAPIUtils
from archipy.configs.base_config import BaseConfig

# Create a FastAPI app with standard config
app = AppUtils.create_fastapi_app(BaseConfig.global_config())

# Add custom exception handlers
FastAPIUtils.add_exception_handlers(app)

# Generate unique route IDs
route_id = FastAPIUtils.generate_unique_route_id("users", "get_user")

# Set up CORS
FastAPIUtils.setup_cors(
    app,
    allowed_origins=["https://example.com"]
)
```

## transaction_utils

Database transaction management:

```python
from archipy.helpers.utils.transaction_utils import TransactionUtils
from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter

# Synchronous transaction
session_manager = SessionManagerAdapter()

with TransactionUtils.atomic_transaction(session_manager):
    # Database operations here
    # Will be committed if successful, rolled back if exception occurs
    pass

# Asynchronous transaction
async with TransactionUtils.async_atomic_transaction(async_session_manager):
    # Async database operations here
    pass
```

## string_utils

String manipulation utilities:

```python
from archipy.helpers.utils.string_utils import StringUtils

# Convert camel case to snake case
snake = StringUtils.camel_to_snake("thisIsACamelCaseString")
print(snake)  # this_is_a_camel_case_string

# Convert snake case to camel case
camel = StringUtils.snake_to_camel("this_is_a_snake_case_string")
print(camel)  # thisIsASnakeCaseString

# Generate a random string
random_str = StringUtils.generate_random_string(length=10)
print(random_str)

# Mask sensitive data
masked = StringUtils.mask_sensitive_data("1234567890123456", show_last=4)
print(masked)  # ************3456
```

## validator_utils

Validate input data:

```python
from archipy.helpers.utils.validator_utils import ValidatorUtils

# Validate email
is_valid_email = ValidatorUtils.is_valid_email("user@example.com")
print(f"Valid email: {is_valid_email}")

# Validate phone number
is_valid_phone = ValidatorUtils.is_valid_phone_number("+15551234567")
print(f"Valid phone: {is_valid_phone}")

# Validate URL
is_valid_url = ValidatorUtils.is_valid_url("https://example.com")
print(f"Valid URL: {is_valid_url}")
```

## keycloak_utils

Authentication and authorization utilities with Keycloak integration:

```python
if __name__ == '__main__':
    import uvicorn
    from uuid import UUID
    from archipy.configs.base_config import BaseConfig
    from archipy.helpers.utils.app_utils import AppUtils
    from archipy.helpers.utils.keycloak_utils import KeycloakUtils
    from archipy.models.types.language_type import LanguageType
    from fastapi import Depends

    # Initialize your app configuration
    config = BaseConfig()
    BaseConfig.set_global(config)
    app = AppUtils.create_fastapi_app()

    # Resource-based authorization for users with role and admin access
    @app.get("/users/{user_uuid}/info")
    def get_user_info(user_uuid: UUID, user: dict = Depends(KeycloakUtils.fastapi_auth(
        resource_type_param="user_uuid",
        resource_type="users",
        required_roles={"user"},
        admin_roles={"superusers", "administrators"},
        lang=LanguageType.EN,
    ))):
        return {
            "message": f"User info for {user_uuid}",
            "username": user.get("preferred_username")
        }

    # Async version for employees with multiple acceptable roles
    @app.get("/employees/{employee_uuid}/info")
    async def get_employee_info(employee_uuid: UUID, employee: dict = Depends(KeycloakUtils.async_fastapi_auth(
        resource_type_param="employee_uuid",
        resource_type="employees",
        required_roles={"employee", "manager", "user"},
        all_roles_required=False,  # User can have any of these roles
        admin_roles={"hr_admins", "system_admins"},
        lang=LanguageType.FA,
    ))):
        return {
            "message": f"Employee info for {employee_uuid}",
            "username": employee.get("preferred_username")
        }

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

# Additional Resources

For more examples and detailed documentation:

- [Helpers Overview](../../api_reference/helpers.md)
- [Utils API Reference](../../api_reference/utils.md)
- [Configuration Examples](../config_management.md)
- [Keycloak Adapter](../adapters/keycloak.md)

> **Note**: This page contains examples of using ArchiPy's utility functions. For API details, see the [Utils API Reference](../../api_reference/utils.md).
