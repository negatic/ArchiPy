"""Environment configuration for behave tests.

This file configures the environment for running BDD tests with behave,
particularly focusing on setup/teardown of resources like databases
and handling async operations.
"""

import asyncio
import logging
import uuid

from behave.model import Scenario
from behave.runner import Context
from features.scenario_context import ScenarioContext
from pydantic_settings import SettingsConfigDict

from archipy.adapters.orm.sqlalchemy.session_manager_registry import SessionManagerRegistry
from archipy.configs.base_config import BaseConfig


class TestConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_file=".env.test",
    )


# Initialize global config
config = TestConfig()
BaseConfig.set_global(config)


def before_all(context: Context):
    """Setup performed before all tests run.

    Args:
        context: The behave context object
    """
    # Configure logging for tests
    logging.basicConfig(level=logging.INFO)
    context.logger = logging.getLogger("behave.tests")
    context.logger.info("Starting test suite")


def after_all(context: Context):
    """Cleanup performed after all tests run.

    Args:
        context: The behave context object
    """
    # Clean up any remaining resources
    context.logger.info("Test suite completed")


def before_feature(context: Context, feature):
    """Setup performed before each feature runs.

    Args:
        context: The behave context object
        feature: The feature about to run
    """
    context.logger.info(f"Starting feature: {feature.name}")


def after_feature(context: Context, feature):
    """Cleanup performed after each feature runs.

    Args:
        context: The behave context object
        feature: The feature that just completed
    """
    context.logger.info(f"Completed feature: {feature.name}")


def before_scenario(context: Context, scenario: Scenario):
    """Setup performed before each scenario runs."""
    # Set up logger
    logger = logging.getLogger("behave.tests")
    context.logger = logger

    # Create a unique ID for this scenario
    scenario_id = getattr(scenario, "_id", uuid.uuid4().hex)

    # Create a scenario-specific context
    context.scenario_context = ScenarioContext(scenario_id)

    logger.info(f"Starting scenario: {scenario.name} (ID: {scenario_id})")

    # Assign global config to scenario context
    try:
        context.scenario_context.store("test_config", BaseConfig.global_config())
    except Exception as e:
        logger.error(f"Error setting global config: {e}")

    # Set up async test environment if needed
    if "async" in scenario.name.lower() or any("async" in tag.lower() for tag in scenario.tags):
        logger.info("Setting up async test environment")
        try:
            # Create a new event loop for this scenario
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            context.scenario_context.store("_async_test_loop", loop)
        except Exception as e:
            logger.error(f"Error setting up async environment: {e}")


def after_scenario(context: Context, scenario: Scenario):
    """Cleanup performed after each scenario runs."""
    logger = getattr(context, "logger", logging.getLogger("behave.environment"))

    # Get the scenario ID
    scenario_id = getattr(scenario, "_id", None)
    logger.info(f"Cleaning up scenario: {scenario.name} (ID: {scenario_id})")

    # Clean up the scenario context
    if hasattr(context, "scenario_context"):
        # Call the cleanup method
        context.scenario_context.cleanup()

        # Clean up async resources
        if "_async_test_loop" in context.scenario_context.storage:
            try:
                loop = context.scenario_context.get("_async_test_loop")
                if loop:
                    # Cancel any pending tasks
                    try:
                        pending_tasks = asyncio.all_tasks(loop)
                        if pending_tasks:
                            for task in pending_tasks:
                                task.cancel()

                            # Use a new event loop for cleanup
                            cleanup_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(cleanup_loop)

                            async def cleanup():
                                pass  # Just a placeholder

                            cleanup_loop.run_until_complete(cleanup())
                            cleanup_loop.close()
                    except Exception as e:
                        logger.error(f"Error cleaning up tasks: {e}")

                    # Close the event loop
                    try:
                        loop.close()
                    except Exception as e:
                        logger.error(f"Error closing event loop: {e}")
            except Exception as e:
                logger.error(f"Error in async cleanup: {e}")

    # Reset the registry
    SessionManagerRegistry.reset()
