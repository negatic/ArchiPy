from behave import then
from behave.runner import Context


@then('an error message "{expected_message}" should be raised')
def step_then_error_message(context: Context, expected_message) -> None:
    assert context.exception_message == expected_message


@then("the validation should {expected_result}")
def step_then_validation_result(context: Context, expected_result) -> None:
    expected_bool = expected_result == "succeed"
    assert context.is_valid == expected_bool


@then('the verification should {expected_result}')
def step_then_verification_succeeds(context: Context, expected_result) -> None:
    expected_bool = expected_result == "succeed"
    assert context.is_verified is expected_bool


@then("the result should be True")
def step_then_result_should_be_true(context: Context) -> None:
    assert context.result is True


@then("the result should be False")
def step_then_result_should_be_false(context: Context) -> None:
    assert context.result is False


@then("the result should be either True or False")
def step_then_result_should_be_boolean(context: Context) -> None:
    assert isinstance(context.result, bool)
