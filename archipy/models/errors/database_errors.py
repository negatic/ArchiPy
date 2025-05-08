from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class DatabaseConnectionError(BaseError):
    """Exception raised for database connection errors."""

    def __init__(
        self,
        database: str | None = None,
        error_details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_CONNECTION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if database:
            data["database"] = database
        if error_details:
            data["error_details"] = error_details
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class DatabaseQueryError(BaseError):
    """Exception raised for database query errors."""

    def __init__(
        self,
        query: str | None = None,
        error_details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_QUERY_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if query:
            data["query"] = query
        if error_details:
            data["error_details"] = error_details
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class DatabaseTransactionError(BaseError):
    """Exception raised for database transaction errors."""

    def __init__(
        self,
        transaction_id: str | None = None,
        error_details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_TRANSACTION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if transaction_id:
            data["transaction_id"] = transaction_id
        if error_details:
            data["error_details"] = error_details
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class StorageError(BaseError):
    """Exception raised for storage access errors."""

    def __init__(
        self,
        storage_type: str | None = None,
        error_details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ErrorDetailDTO = ErrorMessageType.STORAGE_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if storage_type:
            data["storage_type"] = storage_type
        if error_details:
            data["error_details"] = error_details
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class CacheError(BaseError):
    """Exception raised for cache access errors."""

    def __init__(
        self,
        cache_type: str | None = None,
        error_details: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ErrorDetailDTO = ErrorMessageType.CACHE_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if cache_type:
            data["cache_type"] = cache_type
        if error_details:
            data["error_details"] = error_details
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class CacheMissError(BaseError):
    """Exception raised when requested data is not found in cache."""

    def __init__(
        self,
        cache_key: str | None = None,
        lang: LanguageType = LanguageType.FA,
        error: ErrorDetailDTO = ErrorMessageType.CACHE_MISS.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"cache_key": cache_key} if cache_key else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
