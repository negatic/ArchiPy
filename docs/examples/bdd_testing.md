# BDD Testing with ArchiPy

This page demonstrates how to use ArchiPy's integrated BDD testing capabilities with Behave.

## Basic Usage

ArchiPy provides a complete BDD testing setup using Behave. Here's how to use it:

### Feature Files

Create feature files in the `features` directory with Gherkin syntax:

```gherkin
# features/user_management.feature
Feature: User Management
  As a system administrator
  I want to manage users
  So that I can control system access

  Scenario: Create a new user
    Given I have admin privileges
    When I create a user with username "john" and email "john@example.com"
    Then the user should be saved in the database
    And the user should have default permissions
```

### Step Implementations

Implement the steps in Python files under `features/steps`:

```python
# features/steps/user_steps.py
from behave import given, when, then
from app.models import User
from app.services import UserService

@given('I have admin privileges')
def step_impl(context):
    context.is_admin = True

@when('I create a user with username "{username}" and email "{email}"')
def step_impl(context, username, email):
    service = UserService()
    context.user = service.create_user(username, email)

@then('the user should be saved in the database')
def step_impl(context):
    # Check user exists in DB
    db_user = User.query.filter_by(username=context.user.username).first()
    assert db_user is not None

@then('the user should have default permissions')
def step_impl(context):
    assert len(context.user.permissions) > 0
    assert 'user:read' in context.user.permissions
```

### Running Tests

Run BDD tests using the Makefile command:

```bash
make behave
```

To run a specific feature:

```bash
poetry run behave features/user_management.feature
```

To run a specific scenario by line number:

```bash
poetry run behave features/user_management.feature:7
```

This documentation is being migrated from Sphinx to MkDocs format.
Please check back soon for complete content.