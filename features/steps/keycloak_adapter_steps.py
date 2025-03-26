from behave import given, then, when
from features.test_helpers import get_current_scenario_context

from archipy.adapters.keycloak.adapters import KeycloakAdapter


# Store test context
def get_keycloak_adapter(context):
    if not hasattr(context, "keycloak_adapter"):
        # Initialize with test configuration
        scenario_context = get_current_scenario_context(context)
        test_config = scenario_context.get("test_config")
        context.keycloak_adapter = KeycloakAdapter(test_config.KEYCLOAK)
    return context.keycloak_adapter


@given("the Keycloak adapter is initialized with valid configuration")
def step_init_adapter(context):
    get_keycloak_adapter(context)
    context.logger.info("Keycloak adapter initialized")


# Token Operations
@given('a user exists with username "{username}" and password "{password}"')
def step_user_exists(context, username, password):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    try:
        user = adapter.get_user_by_username(username)
        if user:
            adapter.delete_user(user["id"])
        user_data = {
            "username": username,
            "enabled": True,
            "credentials": [{"type": "password", "value": password, "temporary": False}],
        }
        user_id = adapter.create_user(user_data)
        scenario_context.store("user_id", user_id)
        context.logger.info(f"Created user {username} with ID {user_id}")
    except ValueError as e:
        context.logger.error(f"Failed to create user {username}: {e!s}")
        raise


@when('I request a token with username "{username}" and password "{password}"')
def step_request_token(context, username, password):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    try:
        token_response = adapter.get_token(username, password)
        scenario_context.store("token_response", token_response)
    except ValueError as e:
        scenario_context.store("error", str(e))


@then('I receive a valid token response containing "{key1}" and "{key2}"')
def step_verify_token_response(context, key1, key2):
    scenario_context = get_current_scenario_context(context)
    token_response = scenario_context.get("token_response")
    assert token_response is not None, "No token response received"
    assert key1 in token_response, f"{key1} not in token response"
    assert key2 in token_response, f"{key2} not in token response"


@then("I receive an error indicating authentication failed")
def step_verify_auth_error(context):
    scenario_context = get_current_scenario_context(context)
    error = scenario_context.get("error")
    assert error is not None, "Expected an error but none received"
    assert "Failed to get token" in error, "Expected authentication failure message"


@given("I have a valid refresh token")
def step_have_refresh_token(context):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    try:
        token = adapter.get_token("testuser", "password123")
        scenario_context.store("refresh_token", token["refresh_token"])
    except ValueError as e:
        context.logger.error(f"Failed to get refresh token: {e!s}")
        raise


@when("I refresh the token")
def step_refresh_token(context):
    scenario_context = get_current_scenario_context(context)
    adapter = get_keycloak_adapter(context)
    refresh_token = scenario_context.get("refresh_token")
    new_token = adapter.refresh_token(refresh_token)
    scenario_context.store("token_response", new_token)


@given("I have a valid access token")
def step_have_access_token(context):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    try:
        token = adapter.get_token("testuser", "password123")
        scenario_context.store("access_token", token["access_token"])
    except ValueError as e:
        context.logger.error(f"Failed to get access token: {e!s}")
        raise


@when("I validate the token")
def step_validate_token(context):
    scenario_context = get_current_scenario_context(context)
    adapter = get_keycloak_adapter(context)
    token = scenario_context.get("access_token")
    result = adapter.validate_token(token)
    scenario_context.store("validation_result", result)


@then("the validation returns true")
def step_verify_validation(context):
    scenario_context = get_current_scenario_context(context)
    result = scenario_context.get("validation_result")
    assert result is True, "Token validation failed"


# User Management
@given('no user exists with username "{username}"')
def step_no_user_exists(context, username):
    adapter = get_keycloak_adapter(context)
    try:
        user = adapter.get_user_by_username(username)
        if user:
            adapter.delete_user(user["id"])
            context.logger.info(f"Deleted existing user {username}")
    except ValueError as e:
        context.logger.info(f"No user {username} found or deletion failed: {e!s}")


@when('I create a user with username "{username}" and email "{email}"')
def step_create_user(context, username, email):
    adapter = get_keycloak_adapter(context)
    user_data = {"username": username, "email": email, "enabled": True}
    user_id = adapter.create_user(user_data)
    scenario_context = get_current_scenario_context(context)
    scenario_context.store("created_user_id", user_id)


@then("the user is created successfully")
def step_verify_user_created(context):
    scenario_context = get_current_scenario_context(context)
    user_id = scenario_context.get("created_user_id")
    assert user_id is not None, "User creation failed"


@then('I can retrieve the user by username "{username}"')
def step_verify_user_retrieval(context, username):
    adapter = get_keycloak_adapter(context)
    user = adapter.get_user_by_username(username)
    assert user is not None, f"User {username} not found"
    assert user["username"] == username, "Username mismatch"


@given('a user exists with username "{username}"')
def step_user_exists_by_username(context, username):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    try:
        user = adapter.get_user_by_username(username)
        if user:
            adapter.delete_user(user["id"])
        user_data = {"username": username, "enabled": True}
        user_id = adapter.create_user(user_data)
        scenario_context.store("user_id", user_id)
        context.logger.info(f"Created user {username} with ID {user_id}")
    except ValueError as e:
        context.logger.error(f"Failed to create user {username}: {e!s}")
        raise


@when('I request user details by username "{username}"')
def step_get_user_by_username(context, username):
    adapter = get_keycloak_adapter(context)
    user = adapter.get_user_by_username(username)
    scenario_context = get_current_scenario_context(context)
    scenario_context.store("user_details", user)


@then("I receive the user's details")
def step_verify_user_details(context):
    scenario_context = get_current_scenario_context(context)
    user = scenario_context.get("user_details")
    assert user is not None, "No user details received"
    assert "id" in user, "User ID missing"


@when('I update the user\'s email to "{email}"')
def step_update_user(context, email):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    user_id = scenario_context.get("user_id")
    adapter.update_user(user_id, {"email": email})


@then("the user's email is updated successfully")
def step_verify_email_update(context):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    user_id = scenario_context.get("user_id")
    user = adapter.get_user_by_id(user_id)
    assert user["email"] == "updated@example.com", "Email update failed"


# Role Management
@given('a realm role "{role_name}" exists')
def step_role_exists(context, role_name):
    adapter = get_keycloak_adapter(context)
    try:
        adapter.get_realm_role(role_name)
    except ValueError:
        adapter.create_realm_role(role_name, "Test role")


@when('I assign the realm role "{role_name}" to user "{username}"')
def step_assign_role(context, role_name, username):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    user = adapter.get_user_by_username(username)
    user_id = user["id"]
    adapter.assign_realm_role(user_id, role_name)
    scenario_context.store("user_id", user_id)


@then('the user has the role "{role_name}"')
def step_verify_role(context, role_name):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    user_id = scenario_context.get("created_user_id") or scenario_context.get("user_id")
    roles = adapter.get_user_roles(user_id)
    role_names = [role["name"] for role in roles]
    assert role_name in role_names, f"Role {role_name} not assigned"


@given("a user has a valid token")
def step_user_has_token(context):
    step_have_access_token(context)


@given('the user has role "{role_name}"')
def step_user_has_role(context, role_name):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    user_id = scenario_context.get("user_id")
    adapter.assign_realm_role(user_id, role_name)


@when('I check if the token has role "{role_name}"')
def step_check_role(context, role_name):
    scenario_context = get_current_scenario_context(context)
    adapter = get_keycloak_adapter(context)
    token = scenario_context.get("access_token")
    result = adapter.has_role(token, role_name)
    scenario_context.store("role_check", result)


@then("the check returns true")
def step_verify_role_check(context):
    scenario_context = get_current_scenario_context(context)
    result = scenario_context.get("role_check")
    assert result is True, "Role check failed"
