from behave import then


@then('an error message "{expected_message}" should be raised')
def step_then_error_message(context, expected_message):
    assert context.exception_message == expected_message


@then("the validation should {expected_result}")
def step_then_validation_result(context, expected_result):
    expected_bool = expected_result == "succeed"
    assert context.is_valid == expected_bool


@then('the verification should {expected_result}')
def step_then_verification_succeeds(context, expected_result):
    expected_bool = expected_result == "succeed"
    assert context.is_verified is expected_bool
