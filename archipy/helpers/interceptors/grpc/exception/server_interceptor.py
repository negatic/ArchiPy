import logging
from collections.abc import Callable

import grpc
from pydantic import ValidationError

from archipy.helpers.interceptors.grpc.base.server_interceptor import (
    BaseAsyncGrpcServerInterceptor,
    MethodName,
)
from archipy.helpers.utils.base_utils import BaseUtils
from archipy.models.errors import InternalError, InvalidArgumentError
from archipy.models.errors.base_error import BaseError


class AsyncGrpcServerExceptionInterceptor(BaseAsyncGrpcServerInterceptor):
    """An async gRPC server interceptor for centralized exception handling.

    This interceptor catches all exceptions thrown by gRPC service methods and
    converts them to appropriate gRPC errors, eliminating the need for repetitive
    try-catch blocks in each service method.
    """

    def __init__(self, logger: logging.Logger | None = None):
        """Initialize the exception interceptor.

        Args:
            logger: Optional logger instance. If not provided, creates a default logger.
        """
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    async def intercept(
        self, method: Callable, request: object, context: grpc.aio.ServicerContext, method_name_model: MethodName
    ) -> object:
        """Intercepts an async gRPC server call and handles exceptions.

        Args:
            method: The async gRPC method being intercepted.
            request: The request object passed to the method.
            context: The context of the async gRPC call.
            method_name_model: The parsed method name containing package, service, and method components.

        Returns:
            object: The result of the intercepted gRPC method.

        Note:
            This method will not return anything if an exception is handled,
            as the exception handling will abort the gRPC context.
        """
        try:
            # Execute the gRPC method
            result = await method(request, context)
            return result

        except ValidationError as validation_error:
            self._logger.warning(
                f"Validation error in {method_name_model.service}.{method_name_model.method}: {validation_error}"
            )
            await self._handle_validation_error(validation_error, context)

        except BaseError as base_error:
            self._logger.warning(
                f"Business error in {method_name_model.service}.{method_name_model.method}: {base_error}"
            )
            await base_error.abort_grpc_async(context)

        except grpc.aio.AioRpcError:
            # Re-raise gRPC errors as they're already properly formatted
            raise

        except Exception as unexpected_error:
            self._logger.error(
                f"Unexpected error in {method_name_model.service}.{method_name_model.method}: {unexpected_error}",
                exc_info=True,
            )
            await self._handle_unexpected_error(unexpected_error, context, method_name_model)

    async def _handle_validation_error(
        self, validation_error: ValidationError, context: grpc.aio.ServicerContext
    ) -> None:
        """Handle Pydantic validation errors.

        Args:
            validation_error: The validation error to handle.
            context: The gRPC context to abort.
        """
        # Capture the exception for monitoring
        BaseUtils.capture_exception(validation_error)

        # Format validation errors for better debugging
        validation_details = self._format_validation_errors(validation_error)

        await InvalidArgumentError(
            argument_name="request_validation",
            additional_data={"validation_errors": validation_details, "error_count": len(validation_error.errors())},
        ).abort_grpc_async(context)

    @staticmethod
    async def _handle_unexpected_error(
        error: Exception, context: grpc.aio.ServicerContext, method_name_model: MethodName
    ) -> None:
        """Handle unexpected errors by converting them to internal errors.

        Args:
            error: The unexpected error to handle.
            context: The gRPC context to abort.
            method_name_model: The method name information for better error tracking.
        """
        # Capture the exception for monitoring
        BaseUtils.capture_exception(error)

        await InternalError(
            additional_data={
                "original_error": str(error),
                "error_type": type(error).__name__,
                "service": method_name_model.service,
                "method": method_name_model.method,
                "package": method_name_model.package,
            }
        ).abort_grpc_async(context)

    @staticmethod
    def _format_validation_errors(validation_error: ValidationError) -> list[dict[str, str]]:
        """Format Pydantic validation errors into a structured format.

        Args:
            validation_error: The validation error to format.

        Returns:
            A list of formatted validation error details.
        """
        return [
            {
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
                "value": str(error.get("input", "")),
            }
            for error in validation_error.errors()
        ]
