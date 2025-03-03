# Utilities

Examples of ArchiPy's utility functions:

## datetime_utils

Work with dates and times consistently:

```python
from archipy.helpers.utils.datetime_utils import DateTimeUtils

# Get current UTC time
now = DateTimeUtils.get_utc_now()

# Format for storage/transmission
date_str = DateTimeUtils.convert_datetime_to_string(now)

# Parse date string
parsed = DateTimeUtils.convert_string_to_datetime(date_str)

# Convert to Jalali (Persian) calendar
jalali_date = DateTimeUtils.get_jalali_date(now)

# Check if date is a holiday in Iran
is_holiday = DateTimeUtils.is_holiday_in_iran(now)
```

## jwt_utils

Generate and verify JWT tokens:

```python
from archipy.helpers.utils.jwt_utils import JWTUtils
from uuid import uuid4

# Generate a user access token
user_id = uuid4()
access_token = JWTUtils.generate_access_token(user_id)

# Generate a refresh token
refresh_token = JWTUtils.generate_refresh_token(user_id)

# Verify a token
try:
    payload = JWTUtils.verify_jwt(access_token)
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
from archipy.models.types.exception_message_types import ExceptionMessageType

# Create exception detail
detail = ErrorUtils.create_exception_detail(
    ExceptionMessageType.INVALID_PHONE,
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