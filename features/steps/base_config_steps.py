import os

from behave import given, then, when
from features.environment import TestConfig

from archipy.configs.base_config import BaseConfig


@given("a custom BaseConfig instance")
def step_given_custom_base_config(context):
    config = TestConfig()
    BaseConfig.set_global(config)
    context.test_config = BaseConfig.global_config()


@when("the global configuration is set")
def step_when_set_global_config(context):
    BaseConfig.set_global(context.test_config)


@then("retrieving global configuration should return the same instance")
def step_then_check_global_config(context):
    assert BaseConfig.global_config() is context.test_config


@given("BaseConfig is not initialized globally")
def step_given_no_global_config(context):
    BaseConfig._BaseConfig__global_config = None  # Force reset


@when("retrieving global configuration")
def step_when_get_global_config(context):
    try:
        context.global_config = BaseConfig.global_config()
    except AssertionError as e:
        context.error_message = str(e)


@then('an error should be raised with message "{expected_message}"')
def step_then_check_error_message(context, expected_message):
    assert (
        context.error_message == expected_message
    ), f"Expected: '{expected_message}', but got: '{context.error_message}'"


@when("the configuration is initialized")
def step_when_config_is_initialized(context):
    context.instance = TestConfig()


@then('the attribute "{attribute}" should exist')
def step_then_check_attributes(context, attribute):
    assert hasattr(context.instance, attribute), f"Expected attribute '{attribute}' to exist"


@given('an env file with key "{key}" and value "{value}"')
def step_given_env_file_override(context, key, value):
    os.environ[key] = value  # Mock environment variable


@when("BaseConfig is initialized")
def step_when_initialize_base_config(context):
    config = TestConfig()
    BaseConfig.set_global(config)
    context.test_config = BaseConfig.global_config()  # Load settings again


@then('the ENVIRONMENT should be "{expected_value}"')
def step_then_check_environment_variable(context, expected_value):
    assert (
        context.test_config.ENVIRONMENT.name == expected_value
    ), f"Expected '{expected_value}', but got '{context.test_config.ENVIRONMENT.name}'"
