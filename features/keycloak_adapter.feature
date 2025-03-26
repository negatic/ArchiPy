Feature: Keycloak Adapter Operations
  As a system administrator
  I want to manage authentication tokens, users, and roles through the Keycloak adapter
  So that I can secure and control access to my application

  Background:
    Given the Keycloak adapter is initialized with valid configuration

  # Token Operations
  Scenario: Getting a token with valid credentials
    Given a user exists with username "testuser" and password "password123"
    When I request a token with username "testuser" and password "password123"
    Then I receive a valid token response containing "access_token" and "refresh_token"

  Scenario: Getting a token with invalid credentials
    When I request a token with username "invaliduser" and password "wrongpass"
    Then I receive an error indicating authentication failed

  Scenario: Refreshing a valid token
    Given I have a valid refresh token
    When I refresh the token
    Then I receive a valid token response containing "access_token" and "refresh_token"

  Scenario: Validating a token
    Given I have a valid access token
    When I validate the token
    Then the validation returns true

  # User Management
  Scenario: Creating a new user
    Given no user exists with username "newuser"
    When I create a user with username "newuser" and email "newuser@example.com"
    Then the user is created successfully
    And I can retrieve the user by username "newuser"

  Scenario: Getting user by username
    Given a user exists with username "user123"
    When I request user details by username "user123"
    Then I receive the user's details

  Scenario: Updating user information
    Given a user exists with username "updateuser" and password "password123"
    When I update the user's email to "updated@example.com"
    Then the user's email is updated successfully

  # Role Management
  Scenario: Assigning a realm role to a user
    Given a user exists with username "user456"
    And a realm role "test-role" exists
    When I assign the realm role "test-role" to user "user456"
    Then the user has the role "test-role"

  Scenario: Checking user role permissions
    Given a user exists with username "testuser" and password "password123"
    And a realm role "admin" exists
    And the user has role "admin"
    And a user has a valid token
    When I check if the token has role "admin"
    Then the check returns true
