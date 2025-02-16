from behave import given, then, when

from archipy.helpers.utils.base_utils import BaseUtils
from archipy.models.exceptions import (
    InvalidLandlineNumberException,
    InvalidNationalCodeException,
    InvalidPhoneNumberException,
)


@given('an input phone number "{input_number}"')
def step_given_input_phone_number(context, input_number):
    context.input_number = input_number


@when("the phone number is sanitized")
def step_when_sanitize_phone_number(context):
    context.sanitized_output = BaseUtils.sanitize_iranian_landline_or_phone_number(context.input_number)


@then('the sanitized output should be "{expected_output}"')
def step_then_check_sanitized_output(context, expected_output):
    assert context.sanitized_output == expected_output


@given('a valid mobile phone number "{phone_number}"')
def step_given_valid_phone_number(context, phone_number):
    context.phone_number = phone_number


@when("the phone number is validated")
def step_when_validate_phone_number(context):
    context.is_valid = True
    try:
        BaseUtils.validate_iranian_phone_number(context.phone_number)
    except InvalidPhoneNumberException:
        context.is_valid = False


@given('an invalid mobile phone number "{phone_number}"')
def step_given_invalid_phone_number(context, phone_number):
    context.phone_number = phone_number


@when("the phone number validation is attempted")
def step_when_validate_invalid_phone_number(context):
    try:
        BaseUtils.validate_iranian_phone_number(context.phone_number)
    except InvalidPhoneNumberException as e:
        context.exception_message = str(e.message)


@given('a valid landline phone number "{landline_number}"')
def step_given_valid_landline_number(context, landline_number):
    context.landline_number = landline_number


@when("the landline number is validated")
def step_when_validate_landline_number(context):
    context.is_valid = True
    try:
        BaseUtils.validate_iranian_landline_number(context.landline_number)
    except InvalidLandlineNumberException:
        context.is_valid = False


@given('an invalid landline phone number "{landline_number}"')
def step_given_invalid_landline_number(context, landline_number):
    context.landline_number = landline_number


@when("the landline number validation is attempted")
def step_when_validate_invalid_landline_number(context):
    try:
        BaseUtils.validate_iranian_landline_number(context.landline_number)
    except InvalidLandlineNumberException as e:
        context.exception_message = str(e.message)


@given('a valid national code "{national_code}"')
def step_given_valid_national_code(context, national_code):
    context.national_code = national_code


@when("the national code is validated")
def step_when_validate_national_code(context):
    context.is_valid = True
    try:
        BaseUtils.validate_iranian_national_code_pattern(context.national_code)
    except InvalidNationalCodeException:
        context.is_valid = False


@given('an invalid national code "{national_code}"')
def step_given_invalid_national_code(context, national_code):
    context.national_code = national_code


@when("the national code validation is attempted")
def step_when_validate_invalid_national_code(context):
    try:
        BaseUtils.validate_iranian_national_code_pattern(context.national_code)
    except InvalidNationalCodeException as e:
        context.exception_message = str(e.message)
