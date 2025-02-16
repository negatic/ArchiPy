from datetime import datetime, timezone

from behave import given, then, when

from archipy.helpers.utils.datetime_utils import DatetimeUtils


@given('a naive datetime "{date_string}"')
def step_given_naive_datetime(context, date_string):
    context.datetime_obj = datetime.fromisoformat(date_string)


@when("the datetime is ensured to be timezone aware")
def step_when_timezone_ensured(context):
    context.result_datetime = DatetimeUtils.ensure_timezone_aware(context.datetime_obj)


@then("the result should be in UTC timezone")
def step_then_result_should_be_utc(context):
    assert context.result_datetime.tzinfo == timezone.utc


@given('a datetime "{date_string}"')
def step_given_datetime(context, date_string):
    context.datetime_obj = datetime.fromisoformat(date_string)


@when("the datetime is converted to a string")
def step_when_datetime_is_converted(context):
    context.result_string = DatetimeUtils.get_string_datetime_from_datetime(context.datetime_obj)


@then('the resulting string should match the format "{format_string}"')
def step_then_string_should_match_format(context, format_string):
    expected_string = context.datetime_obj.strftime(format_string)
    assert context.result_string == expected_string


@given('a datetime string "{date_string}"')
def step_given_datetime_string(context, date_string):
    context.date_string = date_string


@when("the string is converted to a datetime object")
def step_when_string_to_datetime(context):
    context.result_datetime = DatetimeUtils.get_datetime_from_string_datetime(context.date_string)


@then("the resulting object should be a valid datetime")
def step_then_result_is_datetime(context):
    assert isinstance(context.result_datetime, datetime)


@when("the current UTC time is retrieved")
def step_when_get_current_utc(context):
    context.utc_now = DatetimeUtils.get_datetime_utc_now()


@then("it should be a valid datetime")
def step_then_utc_now_is_datetime(context):
    assert isinstance(context.utc_now, datetime)


@when("the current epoch time is retrieved")
def step_when_get_epoch_now(context):
    context.epoch_now = DatetimeUtils.get_epoch_time_now()


@then("it should be a valid integer timestamp")
def step_then_epoch_is_integer(context):
    assert isinstance(context.epoch_now, int)


@when("1 day is added")
def step_when_add_day(context):
    context.result_datetime = DatetimeUtils.get_datetime_after_given_datetime_or_now(
        days=1,
        datetime_given=context.datetime_obj,
    )


@then('the resulting datetime should be "{expected_date}"')
def step_then_datetime_is_correct(context, expected_date):
    expected_datetime = datetime.fromisoformat(expected_date)
    assert context.result_datetime == expected_datetime


@when("1 day is subtracted")
def step_when_subtract_day(context):
    context.result_datetime = DatetimeUtils.get_datetime_before_given_datetime_or_now(
        days=1,
        datetime_given=context.datetime_obj,
    )
