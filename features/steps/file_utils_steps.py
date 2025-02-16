from behave import given, then, when

from archipy.helpers.utils.file_utils import FileUtils


@given('a valid file path "{file_path}"')
def step_given_valid_file_path(context, file_path):
    context.file_path = file_path


@given("an empty file path")
def step_given_empty_file_path(context):
    context.file_path = ""


@given('a valid file path "{file_path}" and negative minutes')
def step_given_negative_minutes(context, file_path):
    context.file_path = file_path
    context.minutes = -5


@when("a secure link is created")
def step_when_secure_link_created(context):
    context.secure_link = FileUtils.create_secure_link(context.file_path)


@when("a secure link creation is attempted")
def step_when_secure_link_attempted(context):
    try:
        context.secure_link = FileUtils.create_secure_link(context.file_path, getattr(context, "minutes", None))
    except ValueError as e:
        context.exception_message = str(e)


@then("the secure link should contain a hash and expiration timestamp")
def step_then_secure_link_contains_hash(context):
    assert "?md5=" in context.secure_link and "&expires_at=" in context.secure_link


@given('a file name "{file_name}"')
def step_given_file_name(context, file_name):
    context.file_name = file_name


@when("the file name is validated")
def step_when_file_validated(context):
    context.is_valid = FileUtils.validate_file_name(context.file_name)
