Feature: Datetime Utilities

  Scenario: Ensure a timezone-aware datetime
    Given a naive datetime "2024-06-01T10:00:00"
    When the datetime is ensured to be timezone aware
    Then the result should be in UTC timezone

  Scenario: Convert datetime to string format
    Given a datetime "2024-06-01T10:00:00"
    When the datetime is converted to a string
    Then the resulting string should match the format "%Y-%m-%dT%H:%M:%S.%f"

  Scenario: Convert string to datetime
    Given a datetime string "2024-06-01T10:00:00"
    When the string is converted to a datetime object
    Then the resulting object should be a valid datetime

  Scenario: Get current UTC time
    When the current UTC time is retrieved
    Then it should be a valid datetime

  Scenario: Get current epoch time
    When the current epoch time is retrieved
    Then it should be a valid integer timestamp

  Scenario: Add time to a datetime
    Given a datetime "2024-06-01T10:00:00"
    When 1 day is added
    Then the resulting datetime should be "2024-06-02T10:00:00"

  Scenario: Subtract time from a datetime
    Given a datetime "2024-06-01T10:00:00"
    When 1 day is subtracted
    Then the resulting datetime should be "2024-05-31T10:00:00"
