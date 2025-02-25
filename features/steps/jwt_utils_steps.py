import time
from uuid import uuid4

from behave import given, then, when

from archipy.helpers.utils.jwt_utils import JWTUtils
from archipy.models.errors import InvalidTokenError, TokenExpiredError


@given("a valid user UUID")
def step_given_valid_user_uuid(context):
    context.user_uuid = uuid4()


@when("an access token is created")
def step_when_access_token_created(context):
    test_config = context.scenario_context.get("test_config")
    context.token = JWTUtils.create_access_token(context.user_uuid, auth_config=test_config.AUTH)


@when("a refresh token is created")
def step_when_refresh_token_created(context):
    test_config = context.scenario_context.get("test_config")
    context.token = JWTUtils.create_refresh_token(context.user_uuid, auth_config=test_config.AUTH)


@then("a JWT token should be returned")
def step_then_jwt_token_returned(context):
    assert context.token is not None
    assert isinstance(context.token, str)


@given("a valid access token")
def step_given_valid_access_token(context):
    test_config = context.scenario_context.get("test_config")
    context.token = JWTUtils.create_access_token(context.user_uuid, auth_config=test_config.AUTH)


@given("a valid refresh token")
def step_given_valid_refresh_token(context):
    test_config = context.scenario_context.get("test_config")
    context.token = JWTUtils.create_refresh_token(context.user_uuid, auth_config=test_config.AUTH)


@given("an expired access token")
def step_given_expired_access_token(context):
    test_config = context.scenario_context.get("test_config")
    context.token = JWTUtils.create_access_token(
        context.user_uuid,
        additional_claims={"exp": time.time() - 10},
        auth_config=test_config.AUTH,
    )


@given("an invalid token")
def step_given_invalid_token(context):
    context.token = "invalid.token.structure"


@when("the token is decoded")
def step_when_token_decoded(context):
    try:
        test_config = context.scenario_context.get("test_config")
        context.decoded_payload = JWTUtils.decode_token(context.token, auth_config=test_config.AUTH)
        context.decode_success = True
    except Exception as e:
        context.decode_success = False
        context.decode_error = e


@then("the decoded payload should be valid")
def step_then_decoded_payload_valid(context):
    assert context.decode_success is True
    assert isinstance(context.decoded_payload, dict)
    assert "sub" in context.decoded_payload
    assert "type" in context.decoded_payload


@then("a TokenExpiredError should be raised")
def step_then_token_expired_exception_raised(context):
    assert isinstance(context.decode_error, TokenExpiredError)


@then("an InvalidTokenError should be raised")
def step_then_invalid_token_exception_raised(context):
    assert isinstance(context.decode_error, InvalidTokenError)
