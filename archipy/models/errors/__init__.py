"""Error handling module for the application.

This module provides a comprehensive set of custom exceptions for handling various
error scenarios in the application, organized by category.
"""

from archipy.models.errors.auth_errors import (
    AccountDisabledError,
    AccountLockedError,
    InvalidCredentialsError,
    InvalidTokenError,
    InvalidVerificationCodeError,
    PermissionDeniedError,
    SessionExpiredError,
    TokenExpiredError,
    UnauthenticatedError,
)
from archipy.models.errors.base_error import BaseError
from archipy.models.errors.business_errors import (
    BusinessRuleViolationError,
    FailedPreconditionError,
    InsufficientBalanceError,
    InsufficientFundsError,
    InvalidOperationError,
    InvalidStateError,
    MaintenanceModeError,
)
from archipy.models.errors.database_errors import (
    CacheError,
    CacheMissError,
    DatabaseConnectionError,
    DatabaseQueryError,
    DatabaseTransactionError,
    StorageError,
)
from archipy.models.errors.network_errors import (
    BadGatewayError,
    ConnectionTimeoutError,
    GatewayTimeoutError,
    NetworkError,
    RateLimitExceededError,
    ServiceUnavailableError,
)
from archipy.models.errors.resource_errors import (
    AlreadyExistsError,
    ConflictError,
    DataLossError,
    FileTooLargeError,
    InvalidEntityTypeError,
    InvalidFileTypeError,
    NotFoundError,
    QuotaExceededError,
    ResourceBusyError,
    ResourceLockedError,
)
from archipy.models.errors.system_errors import (
    AbortedError,
    ConfigurationError,
    DeadlockDetectedError,
    InternalError,
    ResourceExhaustedError,
    UnavailableError,
    UnknownError,
)
from archipy.models.errors.validation_errors import (
    InvalidArgumentError,
    InvalidDateError,
    InvalidEmailError,
    InvalidFormatError,
    InvalidIpError,
    InvalidJsonError,
    InvalidLandlineNumberError,
    InvalidNationalCodeError,
    InvalidPasswordError,
    InvalidPhoneNumberError,
    InvalidTimestampError,
    InvalidUrlError,
    OutOfRangeError,
)

__all__ = [
    "BaseError",
    # Auth Errors
    "UnauthenticatedError",
    "InvalidCredentialsError",
    "TokenExpiredError",
    "InvalidTokenError",
    "SessionExpiredError",
    "PermissionDeniedError",
    "AccountLockedError",
    "AccountDisabledError",
    "InvalidVerificationCodeError",
    # Validation Errors
    "InvalidArgumentError",
    "InvalidFormatError",
    "InvalidEmailError",
    "InvalidPhoneNumberError",
    "InvalidLandlineNumberError",
    "InvalidNationalCodeError",
    "InvalidPasswordError",
    "InvalidDateError",
    "InvalidUrlError",
    "InvalidIpError",
    "InvalidJsonError",
    "InvalidTimestampError",
    "OutOfRangeError",
    # Resource Errors
    "NotFoundError",
    "AlreadyExistsError",
    "ConflictError",
    "ResourceLockedError",
    "ResourceBusyError",
    "DataLossError",
    "InvalidEntityTypeError",
    "FileTooLargeError",
    "InvalidFileTypeError",
    "QuotaExceededError",
    # Network Errors
    "NetworkError",
    "ConnectionTimeoutError",
    "ServiceUnavailableError",
    "GatewayTimeoutError",
    "BadGatewayError",
    "RateLimitExceededError",
    # Business Errors
    "InvalidStateError",
    "BusinessRuleViolationError",
    "InvalidOperationError",
    "InsufficientFundsError",
    "InsufficientBalanceError",
    "MaintenanceModeError",
    "FailedPreconditionError",
    # Database Errors
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "DatabaseTransactionError",
    "StorageError",
    "CacheError",
    "CacheMissError",
    # System Errors
    "InternalError",
    "ConfigurationError",
    "ResourceExhaustedError",
    "UnavailableError",
    "UnknownError",
    "AbortedError",
    "DeadlockDetectedError",
]
