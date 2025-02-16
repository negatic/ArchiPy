from behave import given, then

from archipy.models.types.exception_message_types import ExceptionMessageType

# Exception Mapping
exception_mapping = {
    "INVALID_PHONE": ExceptionMessageType.INVALID_PHONE,
    "NOT_FOUND": ExceptionMessageType.NOT_FOUND,
    "TOKEN_EXPIRED": ExceptionMessageType.TOKEN_EXPIRED,
}


@given("an exception type \"{exception_enum}\"")
def step_given_exception_type(context, exception_enum):
    context.exception_detail = exception_mapping[exception_enum].value  # Get ExceptionDetailDTO


@then("the exception code should be \"{expected_code}\"")
def step_then_check_exception_code(context, expected_code):
    assert (
        context.exception_detail.code == expected_code
    ), f"Expected '{expected_code}', but got '{context.exception_detail.code}'"


@then("the English message should be \"{expected_message_en}\"")
def step_then_check_english_message(context, expected_message_en):
    assert (
        context.exception_detail.message_en == expected_message_en
    ), f"Expected '{expected_message_en}', but got '{context.exception_detail.message_en}'"


@then("the Persian message should be \"{expected_message_fa}\"")
def step_then_check_persian_message(context, expected_message_fa):
    assert (
        context.exception_detail.message_fa == expected_message_fa
    ), f"Expected '{expected_message_fa}', but got '{context.exception_detail.message_fa}'"


@then("the HTTP status should be {http_status}")
def step_then_check_http_status(context, http_status):
    assert context.exception_detail.http_status == int(
        http_status,
    ), f"Expected HTTP {http_status}, but got {context.exception_detail.http_status}"


@then("the gRPC status should be {grpc_status}")
def step_then_check_grpc_status(context, grpc_status):
    assert context.exception_detail.grpc_status == int(
        grpc_status,
    ), f"Expected gRPC {grpc_status}, but got {context.exception_detail.grpc_status}"
