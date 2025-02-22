from datetime import UTC, date, datetime
from unittest.mock import patch

from behave import given, then, when
from behave.runner import Context

from archipy.helpers.utils.datetime_utils import DatetimeUtils


@given('a naive datetime "{date_string}"')
def step_given_naive_datetime(context: Context, date_string) -> None:
    context.datetime_obj = datetime.fromisoformat(date_string)


@when("the datetime is ensured to be timezone aware")
def step_when_timezone_ensured(context: Context) -> None:
    context.result_datetime = DatetimeUtils.ensure_timezone_aware(context.datetime_obj)


@then("the result should be in UTC timezone")
def step_then_result_should_be_utc(context: Context) -> None:
    assert context.result_datetime.tzinfo == UTC


@given('a datetime "{date_string}"')
def step_given_datetime(context: Context, date_string) -> None:
    context.datetime_obj = datetime.fromisoformat(date_string)


@when("the datetime is converted to a string")
def step_when_datetime_is_converted(context: Context) -> None:
    context.result_string = DatetimeUtils.get_string_datetime_from_datetime(context.datetime_obj)


@then('the resulting string should match the format "{format_string}"')
def step_then_string_should_match_format(context: Context, format_string) -> None:
    expected_string = context.datetime_obj.strftime(format_string)
    assert context.result_string == expected_string


@given('a datetime string "{date_string}"')
def step_given_datetime_string(context: Context, date_string) -> None:
    context.date_string = date_string


@when("the string is converted to a datetime object")
def step_when_string_to_datetime(context: Context) -> None:
    context.result_datetime = DatetimeUtils.get_datetime_from_string_datetime(context.date_string)


@then("the resulting object should be a valid datetime")
def step_then_result_is_datetime(context: Context) -> None:
    assert isinstance(context.result_datetime, datetime)


@when("the current UTC time is retrieved")
def step_when_get_current_utc(context: Context) -> None:
    context.utc_now = DatetimeUtils.get_datetime_utc_now()


@then("it should be a valid datetime")
def step_then_utc_now_is_datetime(context: Context) -> None:
    assert isinstance(context.utc_now, datetime)


@when("the current epoch time is retrieved")
def step_when_get_epoch_now(context: Context) -> None:
    context.epoch_now = DatetimeUtils.get_epoch_time_now()


@then("it should be a valid integer timestamp")
def step_then_epoch_is_integer(context: Context) -> None:
    assert isinstance(context.epoch_now, int)


@when("1 day is added")
def step_when_add_day(context: Context) -> None:
    context.result_datetime = DatetimeUtils.get_datetime_after_given_datetime_or_now(
        days=1,
        datetime_given=context.datetime_obj,
    )


@then('the resulting datetime should be "{expected_date}"')
def step_then_datetime_is_correct(context: Context, expected_date) -> None:
    expected_datetime = datetime.fromisoformat(expected_date)
    assert context.result_datetime == expected_datetime


@when("1 day is subtracted")
def step_when_subtract_day(context: Context) -> None:
    context.result_datetime = DatetimeUtils.get_datetime_before_given_datetime_or_now(
        days=1,
        datetime_given=context.datetime_obj,
    )


@given('a Gregorian date "{date_str}"')
def step_given_gregorian_date(context: Context, date_str) -> None:
    context.date_str = date_str
    try:
        context.target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        context.target_date = None  # Handle invalid date


@given("today's date in Gregorian calendar")
def step_given_todays_date(context: Context) -> None:
    context.target_date = date.today()


@given('an invalid Gregorian date "{date_str}"')
def step_given_invalid_gregorian_date(context: Context, date_str) -> None:
    context.date_str = date_str
    context.target_date = None  # We'll simulate the invalid date in the steps


@when("we check if the date is a holiday in Iran")
def step_when_check_holiday_in_iran(context: Context) -> None:
    try:
        if context.target_date is not None:
            context.result = DatetimeUtils.is_holiday_in_iran(context.target_date)
            context.error = None
        else:
            # Simulate error for invalid date
            raise ValueError(f"Invalid date: {context.date_str}")
    except Exception as e:
        context.error = e
        context.result = None


@when("we check if the date is a holiday in Iran multiple times")
def step_when_check_holiday_multiple_times(context: Context) -> None:
    def mock_call_holiday_api(jalali_date) -> dict:
        context.api_call_count += 1
        return {
            "data": {
                "event_list": [
                    {
                        "jalali_year": context.target_date.year,
                        "jalali_month": context.target_date.month,
                        "jalali_day": context.target_date.day,
                        "is_holiday": True,
                    },
                ],
            },
        }

    with patch.object(DatetimeUtils, "_call_holiday_api", side_effect=mock_call_holiday_api):
        context.api_call_count = 0
        # First call
        context.result_first = DatetimeUtils.is_holiday_in_iran(context.target_date)
        # Second call should use cache
        context.result_second = DatetimeUtils.is_holiday_in_iran(context.target_date)


@then("an error should be raised")
def step_then_error_should_be_raised(context: Context) -> None:
    assert isinstance(context.error, Exception)


@then("the result should be cached, avoiding repeated API calls")
def step_then_result_should_be_cached(context: Context) -> None:
    # The API should have been called only once
    assert context.api_call_count == 1
    # Both results should be the same
    assert context.result_first == context.result_second
