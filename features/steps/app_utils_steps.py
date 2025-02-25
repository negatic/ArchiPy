from behave import given, then, when
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel, ValidationError
from starlette.testclient import TestClient

from archipy.helpers.utils.app_utils import AppUtils, FastAPIExceptionHandler, FastAPIUtils
from archipy.models.errors import BaseError


@given("a FastAPI app")
def step_given_fastapi_app(context):
    # Get config from scenario_context instead of directly from context
    test_config = context.scenario_context.get("test_config")
    context.app = AppUtils.create_fastapi_app(test_config)


@when("a FastAPI app is created")
def step_when_fastapi_app_created(context):
    # Get config from scenario_context instead of directly from context
    test_config = context.scenario_context.get("test_config")
    context.app = AppUtils.create_fastapi_app(test_config)


@then("the app should have the correct title")
def step_then_check_app_title(context):
    assert context.app.title == "Test API"


@then("exception handlers should be registered")
def step_then_check_exception_handlers(context):
    assert BaseError in context.app.exception_handlers
    assert ValidationError in context.app.exception_handlers


@given('a FastAPI route with tag "{tag}" and name "{route_name}"')
def step_given_fastapi_route(context, tag, route_name):
    context.route = APIRoute(path="/users", endpoint=lambda: None, name=route_name, tags=[tag])


@when("a unique ID is generated")
def step_when_generate_unique_id(context):
    context.unique_id = FastAPIUtils.custom_generate_unique_id(context.route)


@then('the unique ID should be "{expected_id}"')
def step_then_check_unique_id(context, expected_id):
    assert context.unique_id == expected_id


@given("a FastAPI app with CORS configuration")
def step_given_fastapi_app_with_cors(context):
    context.app = FastAPI()
    # Get config from scenario_context instead of directly from context
    test_config = context.scenario_context.get("test_config")
    FastAPIUtils.setup_cors(context.app, test_config)


@when("CORS middleware is setup")
def step_when_cors_is_setup(context):
    context.middleware_stack = {middleware.cls.__name__ for middleware in context.app.user_middleware}


@then('the app should allow origins "{expected_origin}"')
def step_then_check_cors_origin(context, expected_origin):
    # Get config from scenario_context instead of directly from context
    test_config = context.scenario_context.get("test_config")
    assert "CORSMiddleware" in context.middleware_stack
    assert expected_origin in test_config.FASTAPI.CORS_MIDDLEWARE_ALLOW_ORIGINS


@when('an endpoint raises a "{exception_type}"')
def step_when_endpoint_raises_exception(context, exception_type):
    context.app.add_exception_handler(
        eval(exception_type),
        FastAPIExceptionHandler.custom_exception_handler,
    )

    @context.app.get("/test-exception")
    def raise_exception():
        raise eval(exception_type)()

    client = TestClient(context.app)
    context.response = client.get("/test-exception")


@then("the response should have status code 500")
def step_then_check_500_error(context):
    assert context.response.status_code == 500


@when("an endpoint raises a validation error")
def step_when_endpoint_raises_validation_error(context):
    context.app.add_exception_handler(ValidationError, FastAPIExceptionHandler.validation_exception_handler)

    class TestSchema(BaseModel):
        id: int

    @context.app.get("/test-validation")
    def validate_data(schema: TestSchema = Depends()):
        return {"message": "Valid"}

    client = TestClient(context.app)
    context.response = client.get("/test-validation", params={"id": "invalid"})


@then("the response should have status code 422")
def step_then_check_422_error(context):
    assert context.response.status_code == 422
