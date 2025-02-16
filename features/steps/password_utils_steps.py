from behave import given, then, when

from archipy.helpers.utils.password_utils import PasswordUtils


@given('a password "{password}"')
def step_given_password(context, password):
    context.password = password


@given('the password is hashed')
def step_given_password_hashed(context):
    context.hashed_password = PasswordUtils.hash_password(context.password, context.test_config.AUTH)


@when('the password is hashed')
def step_when_password_hashed(context):
    context.hashed_password = PasswordUtils.hash_password(context.password, context.test_config.AUTH)


@then('a hashed password should be returned')
def step_then_hashed_password_returned(context):
    assert context.hashed_password is not None
    assert isinstance(context.hashed_password, str)


@when('the password is verified')
def step_when_password_verified(context):
    context.is_verified = PasswordUtils.verify_password(
        context.password,
        context.hashed_password,
        context.test_config.AUTH,
    )


@when('a different password "{wrong_password}" is verified')
def step_when_wrong_password_verified(context, wrong_password):
    context.is_verified = PasswordUtils.verify_password(
        wrong_password,
        context.hashed_password,
        context.test_config.AUTH,
    )


@when('the password is validated')
def step_when_password_validated(context):
    try:
        PasswordUtils.validate_password(context.password, context.test_config.AUTH)
        context.validation_passed = True
    except ValueError as e:
        context.validation_passed = False
        context.validation_error = str(e)


@then("the password validation should succeed")
def step_then_validation_succeeds(context):
    assert context.validation_passed is True


@then("the password validation should fail")
def step_then_validation_fails_with_message(context):
    assert context.validation_passed is False
    assert context.validation_error is not None


@when('a secure password is generated')
def step_when_secure_password_generated(context):
    context.generated_password = PasswordUtils.generate_password(context.test_config.AUTH)


@then('the generated password should meet security requirements')
def step_then_secure_password_meets_requirements(context):
    assert len(context.generated_password) >= context.test_config.AUTH.MIN_LENGTH
    assert any(char.isdigit() for char in context.generated_password)
    assert any(char.islower() for char in context.generated_password)
    assert any(char.isupper() for char in context.generated_password)
    assert any(char in context.test_config.AUTH.SPECIAL_CHARACTERS for char in context.generated_password)


@given('a password history containing "{old_password}"')
def step_given_password_history(context, old_password):
    context.password_history = [PasswordUtils.hash_password(old_password, context.test_config.AUTH)]


@when('a user attempts to reuse "{new_password}" as a new password')
def step_when_reuse_old_password(context, new_password):
    try:
        PasswordUtils.validate_password_history(new_password, context.password_history, context.test_config.AUTH)
        context.validation_passed = True
    except ValueError as e:
        context.validation_passed = False
        context.validation_error = str(e)


@then("the password validation should fail with an error message")
def step_then_password_reuse_fails_with_message(context):
    assert context.validation_passed is False
    assert "Password has been used recently" in context.validation_error
