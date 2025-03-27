# features/steps/keycloak_auth_steps.py
from behave import given, then, when
from features.test_helpers import get_current_scenario_context, safe_run_async

from archipy.adapters.keycloak.adapters import AsyncKeycloakAdapter, KeycloakAdapter


def get_keycloak_adapter(context):
    """Get or initialize the appropriate Keycloak adapter based on scenario tags."""
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    if is_async:
        if not hasattr(scenario_context, "async_adapter") or scenario_context.async_adapter is None:
            test_config = scenario_context.get("test_config")
            scenario_context.async_adapter = AsyncKeycloakAdapter(test_config.KEYCLOAK)
        return scenario_context.async_adapter
    if not hasattr(scenario_context, "adapter") or scenario_context.adapter is None:
        test_config = scenario_context.get("test_config")
        scenario_context.adapter = KeycloakAdapter(test_config.KEYCLOAK)
    return scenario_context.adapter


@given('a Keycloak realm "{realm}" exists')
def step_realm_exists(context, realm):
    context.logger.info(f"Assuming Keycloak realm '{realm}' exists")


@given('a client "{client_id}" exists')
def step_client_exists(context, client_id):
    context.logger.info(f"Assuming client '{client_id}' exists")


@given('the "VERIFY_PROFILE" required action is disabled in realm "{realm}"')
def step_verify_profile_disabled(context, realm):
    context.logger.info(f"Assuming 'VERIFY_PROFILE' required action is disabled in realm '{realm}'")


@given('client "{client_id}" has client authentication enabled')
def step_client_auth_enabled(context, client_id):
    context.logger.info(f"Assuming client '{client_id}' has client authentication enabled")


@given('client "{client_id}" has service accounts roles enabled')
def step_service_accounts_enabled(context, client_id):
    context.logger.info(f"Assuming client '{client_id}' has service accounts roles enabled")


@given('client "{client_id}" has "{role1}" and "{role2}" service account role access')
def step_service_account_roles(context, client_id, role1, role2):
    context.logger.info(f"Assuming client '{client_id}' has '{role1}' and '{role2}' service account role access")


@given("a configured {adapter_type} Keycloak adapter")
def step_configured_adapter(context, adapter_type):
    get_keycloak_adapter(context)
    context.logger.info(f"{adapter_type.capitalize()} Keycloak adapter configured")


@given('a user exists with username "{username}" and password "{password}"')
def step_user_exists(context, username, password):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    user_data = {
        "username": username,
        "enabled": True,
        "credentials": [{"type": "password", "value": password, "temporary": False}],
    }

    try:
        if is_async:

            async def create_user_async(context):
                user = await adapter.get_user_by_username(username)
                if user:
                    await adapter.delete_user(user["id"])
                user_id = await adapter.create_user(user_data)
                scenario_context.store(f"user_id_{username}", user_id)

            safe_run_async(create_user_async)(context)
        else:
            user = adapter.get_user_by_username(username)
            if user:
                adapter.delete_user(user["id"])
            user_id = adapter.create_user(user_data)
            scenario_context.store(f"user_id_{username}", user_id)
        context.logger.info(f"Created user {username} with ID {scenario_context.get(f'user_id_{username}')}")
    except Exception as e:
        context.logger.error(f"Failed to create user {username}: {e!s}")
        raise


@given('I have a valid token for "{username}" with password "{password}" using {adapter_type} adapter')
def step_have_valid_token(context, username, password, adapter_type):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    if is_async:

        async def get_token_async(context):
            token_response = await adapter.get_token(username, password)
            scenario_context.store(f"token_response_{username}", token_response)

        safe_run_async(get_token_async)(context)
    else:
        token_response = adapter.get_token(username, password)
        scenario_context.store(f"token_response_{username}", token_response)
    context.logger.info(f"Obtained initial token for {username}")


# Action steps
@when('I request a token with username "{username}" and password "{password}" using {adapter_type} adapter')
def step_request_token(context, username, password, adapter_type):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    try:
        if is_async:

            async def request_token_async(context):
                token_response = await adapter.get_token(username, password)
                scenario_context.store("latest_token_response", token_response)

            safe_run_async(request_token_async)(context)
        else:
            token_response = adapter.get_token(username, password)
            scenario_context.store("latest_token_response", token_response)
        context.logger.info(f"Requested token for {username}")
    except Exception as e:
        scenario_context.store("token_error", str(e))
        context.logger.error(f"Token request failed: {e!s}")


@when("I refresh the token using {adapter_type} adapter")
def step_refresh_token(context, adapter_type):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    prev_step = next(s for s in reversed(context.scenario.steps) if "have a valid token" in s.name)
    username = prev_step.name.split('"')[1]
    refresh_token = scenario_context.get(f"token_response_{username}")["refresh_token"]

    if is_async:

        async def refresh_token_async(context):
            new_token = await adapter.refresh_token(refresh_token)
            scenario_context.store("latest_token_response", new_token)

        safe_run_async(refresh_token_async)(context)
    else:
        new_token = adapter.refresh_token(refresh_token)
        scenario_context.store("latest_token_response", new_token)
    context.logger.info(f"Refreshed token for {username}")


@when("I request user info with the token using {adapter_type} adapter")
def step_request_user_info(context, adapter_type):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    prev_step = next(s for s in reversed(context.scenario.steps) if "have a valid token" in s.name)
    username = prev_step.name.split('"')[1]
    access_token = scenario_context.get(f"token_response_{username}")["access_token"]

    if is_async:

        async def get_userinfo_async(context):
            user_info = await adapter.get_userinfo(access_token)
            scenario_context.store("latest_user_info", user_info)

        safe_run_async(get_userinfo_async)(context)
    else:
        user_info = adapter.get_userinfo(access_token)
        scenario_context.store("latest_user_info", user_info)
    context.logger.info(f"Requested user info for {username}")


@when("I logout the user using {adapter_type} adapter")
def step_logout_user(context, adapter_type):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    prev_step = next(s for s in reversed(context.scenario.steps) if "have a valid token" in s.name)
    username = prev_step.name.split('"')[1]
    refresh_token = scenario_context.get(f"token_response_{username}")["refresh_token"]

    if is_async:

        async def logout_async(context):
            result = await adapter.logout(refresh_token)
            scenario_context.store("logout_result", result)

        safe_run_async(logout_async)(context)
    else:
        result = adapter.logout(refresh_token)
        scenario_context.store("logout_result", result)
    context.logger.info(f"Logged out user {username}")


@when("I validate the token using {adapter_type} adapter")
def step_validate_token(context, adapter_type):
    adapter = get_keycloak_adapter(context)
    scenario_context = get_current_scenario_context(context)
    is_async = "async" in context.scenario.tags

    prev_step = next(s for s in reversed(context.scenario.steps) if "have a valid token" in s.name)
    username = prev_step.name.split('"')[1]
    access_token = scenario_context.get(f"token_response_{username}")["access_token"]

    if is_async:

        async def validate_async(context):
            result = await adapter.introspect_token(access_token)
            scenario_context.store("validation_result", result)

        safe_run_async(validate_async)(context)
    else:
        result = adapter.introspect_token(access_token)
        scenario_context.store("validation_result", result)
    context.logger.info(f"Validated token for {username}")


# Verification steps
@then("the {adapter_type} token request should succeed")
def step_token_request_succeeds(context, adapter_type):
    scenario_context = get_current_scenario_context(context)
    token_response = scenario_context.get("latest_token_response")
    assert token_response is not None, f"{adapter_type.capitalize()} token request failed"
    assert "access_token" in token_response, "Access token missing"
    context.logger.info(f"{adapter_type.capitalize()} token request verified")


@then("the {adapter_type} token refresh should succeed")
def step_token_refresh_succeeds(context, adapter_type):
    scenario_context = get_current_scenario_context(context)
    token_response = scenario_context.get("latest_token_response")
    assert token_response is not None, f"{adapter_type.capitalize()} token refresh failed"
    assert "access_token" in token_response, "Refreshed access token missing"
    context.logger.info(f"{adapter_type.capitalize()} token refresh verified")


@then('the {adapter_type} token response should contain "{field1}" and "{field2}"')
def step_token_response_contains(context, adapter_type, field1, field2):
    scenario_context = get_current_scenario_context(context)
    token_response = scenario_context.get("latest_token_response")
    assert field1 in token_response, f"{field1} missing from {adapter_type} token response"
    assert field2 in token_response, f"{field2} missing from {adapter_type} token response"
    context.logger.info(f"{adapter_type.capitalize()} token response fields verified")


@then("the {adapter_type} user info request should succeed")
def step_user_info_succeeds(context, adapter_type):
    scenario_context = get_current_scenario_context(context)
    user_info = scenario_context.get("latest_user_info")
    assert user_info is not None, f"{adapter_type.capitalize()} user info request failed"
    context.logger.info(f"{adapter_type.capitalize()} user info request verified")


@then('the {adapter_type} user info should contain "{field1}" and "{field2}"')
def step_user_info_contains(context, adapter_type, field1, field2):
    scenario_context = get_current_scenario_context(context)
    user_info = scenario_context.get("latest_user_info")
    assert field1 in user_info, f"{field1} missing from {adapter_type} user info"
    assert field2 in user_info, f"{field2} missing from {adapter_type} user info"
    context.logger.info(f"{adapter_type.capitalize()} user info fields verified")


@then("the {adapter_type} logout operation should succeed")
def step_logout_succeeds(context, adapter_type):
    scenario_context = get_current_scenario_context(context)
    result = scenario_context.get("logout_result")
    assert result is True or result is None, f"{adapter_type.capitalize()} logout failed"
    context.logger.info(f"{adapter_type.capitalize()} logout verified")


@then("the {adapter_type} token validation should succeed")
def step_token_validation_succeeds(context, adapter_type):
    scenario_context = get_current_scenario_context(context)
    result = scenario_context.get("validation_result")
    assert result is not None, f"{adapter_type.capitalize()} token validation failed"
    assert result.get("active", False), "Token is not active"
    context.logger.info(f"{adapter_type.capitalize()} token validation verified")
