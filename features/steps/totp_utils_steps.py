from behave import given, then, when

from archipy.helpers.utils.totp_utils import TOTPUtils


@given('a valid secret "{secret}"')
def step_given_valid_secret(context, secret):
    context.secret = secret


@given("a TOTP code is generated")
def step_given_totp_generated(context):
    context.totp_code, context.expires = TOTPUtils.generate_totp(context.secret, context.test_config.AUTH)


@given('an invalid TOTP code "{totp_code}"')
def step_given_invalid_totp_code(context, totp_code):
    context.invalid_totp_code = totp_code


@when("a TOTP is generated")
def step_when_totp_generated(context):
    context.totp_code, context.expires = TOTPUtils.generate_totp(context.secret, context.test_config.AUTH)


@when("the TOTP code is verified")
def step_when_totp_verified(context):
    context.is_verified = TOTPUtils.verify_totp(context.secret, context.totp_code, context.test_config.AUTH)


@when("the invalid TOTP code is verified")
def step_when_invalid_totp_verified(context):
    context.is_verified = TOTPUtils.verify_totp(context.secret, context.invalid_totp_code, context.test_config.AUTH)


@when("a secret key is generated")
def step_when_secret_key_generated(context):
    context.secret_key = TOTPUtils.generate_secret_key_for_totp(context.test_config.AUTH)


@then("a TOTP code is returned")
def step_then_totp_code_returned(context):
    assert context.totp_code.isdigit()


@then("an expiration time is provided")
def step_then_expiration_time_provided(context):
    assert context.expires is not None


@then("a secret key is returned")
def step_then_secret_key_returned(context):
    assert context.secret_key is not None
