import asyncio
from http import HTTPStatus
from unittest.mock import patch

from behave import given, then, when
from fastapi.responses import JSONResponse
from grpc import StatusCode

from archipy.helpers.utils.exception_utils import ExceptionUtils
from archipy.models.dtos.exception_dto import ExceptionDetailDTO
from archipy.models.exceptions import CommonsBaseException, InvalidPhoneNumberException, NotFoundException


@given('a raised exception "{exception_type}" with message "{message}"')
def step_given_raised_exception(context, exception_type, message):
    context.exception = eval(f"{exception_type}('{message}')")


@when("the exception is captured")
def step_when_exception_is_captured(context):
    with patch("logging.exception") as mock_log:
        ExceptionUtils.capture_exception(context.exception)
        context.log_called = mock_log.called  # Capture whether logging.exception was called


@then("it should be logged")
def step_then_exception_should_be_logged(context):
    assert context.log_called is True


@given('an exception with code "{code}", English message "{message_en}", and Persian message "{message_fa}"')
def step_given_create_exception_detail(context, code, message_en, message_fa):
    context.exception_details = ExceptionDetailDTO.create_exception_detail(code, message_en, message_fa)


@when("an exception detail is created")
def step_when_exception_detail_is_created(context):
    pass  # No need for additional processing


@then('the response should contain code "{expected_code}"')
def step_then_exception_detail_should_contain_code(context, expected_code):
    assert context.exception_details.code == expected_code


@given('a FastAPI exception "{exception_type}"')
def step_given_fastapi_exception(context, exception_type):
    context.fastapi_exception = eval(f"{exception_type}()")


@when("an async FastAPI exception is handled")
def step_when_fastapi_exception_is_handled(context):
    async def handle_exception():
        return await ExceptionUtils.async_handle_fastapi_exception(None, context.fastapi_exception)

    with patch("fastapi.responses.JSONResponse") as mock_response:
        mock_response.return_value = JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": "Error occurred"},  # Provide required content
        )
        context.http_status = asyncio.run(handle_exception()).status_code


@then("the response should have an HTTP status of 500")
def step_then_http_status_should_be_500(context):
    assert context.http_status == 500


@given('a gRPC exception "{exception_type}"')
def step_given_grpc_exception(context, exception_type):
    context.grpc_exception = eval(f"{exception_type}()")


@when("gRPC exception is handled")
def step_when_grpc_exception_is_handled(context):
    context.grpc_code, _ = ExceptionUtils.handle_grpc_exception(context.grpc_exception)


@then('the response should have gRPC status "UNKNOWN"')
def step_then_grpc_status_should_be_unknown(context):
    assert context.grpc_code == StatusCode.UNKNOWN.value[0]


@given("a list of FastAPI exceptions {exception_names}")
def step_given_list_of_exceptions(context, exception_names):
    # Define an exception mapping from names to actual classes
    exception_mapping = {
        "InvalidPhoneNumberException": InvalidPhoneNumberException,
        "NotFoundException": NotFoundException,
        "CommonsBaseException": CommonsBaseException,
    }
    # Convert exception names into actual class references
    context.exception_list = [
        exception_mapping[exc.strip()]
        for exc in exception_names.strip('[]').split(",")
        if exc.strip() in exception_mapping
    ]


@when("the FastAPI exception responses are generated")
def step_when_generate_exception_responses(context):
    context.responses = ExceptionUtils.get_fastapi_exception_responses(context.exception_list)


@then("the responses should contain HTTP status codes")
def step_then_responses_should_contain_status_codes(context):
    assert isinstance(context.responses, dict)
    assert len(context.responses) > 0, "Expected non-empty responses, but got empty dictionary."
    assert any(isinstance(status, HTTPStatus) for status in context.responses.keys()), "No valid HTTPStatus keys found."
