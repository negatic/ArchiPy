from behave import given, then, when

from archipy.helpers.utils.string_utils import StringUtils


@given('a text with Arabic vowels "{text}"')
def step_given_text_with_arabic_vowels(context, text):
    context.test_text = text


@when("the Arabic vowels are removed")
def step_when_arabic_vowels_removed(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text)


@then('the resulting text should be "{expected_text}"')
def step_then_resulting_text_should_be(context, expected_text):
    assert context.result_text == expected_text


@given('a text with unnormalized Persian characters "{text}"')
def step_given_persian_chars(context, text):
    context.test_text = text


@when("the Persian characters are normalized")
def step_when_persian_chars_normalized(context):
    context.result_text = StringUtils.normalize_persian_chars(context.test_text)


@given('a text with mixed punctuation "{text}"')
def step_given_text_with_punctuation(context, text):
    context.test_text = text


@when("the punctuation is normalized")
def step_when_punctuation_normalized(context):
    context.result_text = StringUtils.normalize_punctuation(context.test_text)


@given('a text with Persian numbers "{text}"')
def step_given_text_with_persian_numbers(context, text):
    context.test_text = text


@when("the numbers are normalized")
def step_when_numbers_normalized(context):
    context.result_text = StringUtils.normalize_numbers(context.test_text)


@given('a text containing numbers "{text}"')
def step_given_text_with_numbers(context, text):
    context.test_text = text


@when("numbers are replaced with a mask")
def step_when_numbers_replaced_with_mask(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text, mask_all_numbers=True)


@given('a text containing currency symbols "{text}"')
def step_given_text_with_currency(context, text):
    context.test_text = text


@when("currencies are replaced with a mask")
def step_when_currencies_replaced_with_mask(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text, mask_currencies=True)


@given('an empty string "{text}"')
def step_given_empty_string(context, text):
    context.test_text = text


@given("a None string")
def step_given_none_string(context):
    context.test_text = None


@when("checking if the string is empty")
def step_when_checking_empty_string(context):
    context.result = StringUtils.is_string_none_or_empty(context.test_text)


@given('a complex text "{text}"')
def step_given_complex_text(context, text):
    context.test_text = text


@when("full text normalization is applied")
def step_when_text_is_normalized(context):
    context.result_text = StringUtils.normalize_persian_text(
        context.test_text,
        remove_vowels=True,
        normalize_punctuation=True,
        normalize_numbers=True,
        normalize_persian_chars=True,
        clean_spacing=True,
        remove_emojis=True,
    )


@given('a text with spacing issues "{text}"')
def step_given_text_with_spacing_issues(context, text):
    context.test_text = text


@when("the spacing is cleaned")
def step_when_spacing_cleaned(context):
    context.result_text = StringUtils.clean_spacing(context.test_text)


@given('a text with punctuation "{text}"')
def step_given_text_with_punctuation_marks(context, text):
    context.test_text = text


@when("the punctuation is removed")
def step_when_punctuation_removed(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text, remove_punctuation=True)


@given('a text containing a URL "{text}"')
def step_given_text_with_url(context, text):
    context.test_text = text


@when("URLs are masked")
def step_when_urls_masked(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text, mask_urls=True)


@given('a text containing an email "{text}"')
def step_given_text_with_email(context, text):
    context.test_text = text


@when("emails are masked")
def step_when_emails_masked(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text, mask_emails=True)


@given('a text containing a phone number "{text}"')
def step_given_text_with_phone(context, text):
    context.test_text = text


@when("phone numbers are masked")
def step_when_phone_numbers_masked(context):
    context.result_text = StringUtils.normalize_persian_text(context.test_text, mask_phones=True)


@given('a text with English numbers "{text}"')
def step_given_text_with_english_numbers(context, text):
    context.test_text = text


@when("the English numbers are converted to Persian")
def step_when_english_numbers_converted(context):
    context.result_text = StringUtils.convert_english_number_to_persian(context.test_text)


@given('a text containing emojis "{text}"')
def step_given_text_with_emojis(context, text):
    context.test_text = text


@when("emojis are removed")
def step_when_emojis_removed(context):
    context.result_text = StringUtils.remove_emoji(context.test_text)
