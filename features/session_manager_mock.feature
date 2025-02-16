Feature: SQLAlchemy Mock Database Operations and Session Management

  Scenario: Ensure SessionManagerMock is a Singleton
    Given a SessionManagerMock instance
    When another SessionManagerMock instance is created
    Then both instances should be the same

  Scenario: Ensure AsyncSessionManagerMock is a Singleton
    Given an AsyncSessionManagerMock instance
    When another AsyncSessionManagerMock instance is created
    Then both instances should be the same

  Scenario: Ensure a session is created and removed properly
    Given a SessionManagerMock instance
    When a session is acquired
    Then the session should not be None
    When the session is removed
    Then acquiring a new session should not be the same as the previous one

  Scenario: Ensure an async session is created and removed properly
    Given an AsyncSessionManagerMock instance
    When an async session is acquired
    Then the async session should not be None
    When the async session is removed
    Then acquiring a new async session should not be the same as the previous one

  Scenario: Verify SQLite engine creation
    Given a SessionManagerMock instance
    When an SQLite engine is created
    Then the engine connection should be successful

  Scenario: Verify Async SQLite engine creation
    Given an AsyncSessionManagerMock instance
    When an Async SQLite engine is created
    Then the async engine connection should be successful

  Scenario: Ensure entity lifecycle management
    Given a adapter is acquired
    When an SQLite test database is set up
    And a new entity is created and saved
    Then the entity should be retrievable
    When the entity is deleted
    Then retrieving it should return None
# todo fix it
#  Scenario: Ensure async entity lifecycle management
#    Given a async adapter is acquired
#    When an async SQLite test database is set up
#    And an async new entity is created and saved
#    Then the async entity should be retrievable
#    When the async entity is deleted
#    Then async retrieving it should return None
