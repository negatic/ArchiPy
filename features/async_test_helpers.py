"""This module provides utilities to help with async testing in behave.

It focuses on solving the problem of SQLAlchemy async scoped sessions
using current_task() for scoping, which can cause issues in behave tests.
"""

import asyncio
import functools
import logging

from behave.runner import Context

from archipy.models.entities import BaseEntity


def safe_has_attr(obj, attr):
    """A truly safe way to check if an attribute exists on an object.

    This uses the __dict__ directly rather than hasattr() which can
    trigger __getattr__ and raise exceptions.

    Args:
        obj: The object to check
        attr: The attribute name to check for

    Returns:
        bool: True if the attribute exists, False otherwise
    """
    # For Context objects in behave, check the dictionary directly
    if hasattr(obj, "__dict__"):
        return attr in obj.__dict__

    # Fallback to normal hasattr for other objects
    try:
        return hasattr(obj, attr)
    except:
        return False


def safe_get_attr(obj, attr, default=None):
    """A truly safe way to get an attribute from an object.

    This uses the __dict__ directly rather than getattr() which can
    trigger __getattr__ and raise exceptions.

    Args:
        obj: The object to get the attribute from
        attr: The attribute name to get
        default: The default value to return if the attribute doesn't exist

    Returns:
        The attribute value, or the default if it doesn't exist
    """
    # For Context objects in behave, check the dictionary directly
    if hasattr(obj, "__dict__"):
        return obj.__dict__.get(attr, default)

    # Fallback to normal getattr for other objects
    try:
        return getattr(obj, attr, default)
    except:
        return default


def safe_set_attr(obj, attr, value):
    """A truly safe way to set an attribute on an object.

    This uses the __dict__ directly rather than setattr() which can
    trigger __getattr__ and raise exceptions.

    Args:
        obj: The object to set the attribute on
        attr: The attribute name to set
        value: The value to set
    """
    # For Context objects in behave, set the dictionary directly
    if hasattr(obj, "__dict__"):
        obj.__dict__[attr] = value
    else:
        # Fallback to normal setattr for other objects
        setattr(obj, attr, value)


def safe_run_async(func):
    """A more robust decorator for running async functions in behave steps.

    This decorator handles attribute access safely and provides better error handling.

    Args:
        func: The async function to wrap

    Returns:
        A wrapped function that safely runs the async function
    """

    @functools.wraps(func)
    def wrapper(context, *args, **kwargs):
        logger = safe_get_attr(context, "logger", logging.getLogger("behave.async_test"))

        # Safely get or create an event loop
        if (
            not safe_has_attr(context, "_async_test_loop")
            or safe_get_attr(context, "_async_test_loop") is None
            or safe_get_attr(safe_get_attr(context, "_async_test_loop", object()), "is_closed", lambda: True)()
        ):
            logger.info("Creating new event loop for test")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            safe_set_attr(context, "_async_test_loop", loop)
        else:
            loop = safe_get_attr(context, "_async_test_loop")
            asyncio.set_event_loop(loop)

        # Run the async function
        async def run_func():
            # Set main task if it doesn't exist
            if not safe_has_attr(context, "_main_task"):
                safe_set_attr(context, "_main_task", asyncio.current_task())

            # Make sure we have the async adapter available
            if not hasattr(context.scenario_context, "async_adapter") or context.scenario_context.async_adapter is None:
                logger.error("No async adapter available in the scenario context")
                raise RuntimeError("Async adapter not properly configured")

            try:
                return await func(context, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error in async function execution: {e}")
                # Print detailed exception info for debugging
                import traceback

                logger.error(traceback.format_exc())
                raise

        try:
            return loop.run_until_complete(run_func())
        except Exception as e:
            logger.error(f"Error running async function: {e}")
            raise

    return wrapper


class SafeAsyncContextManager:
    """A more robust async context manager for Behave tests.

    This context manager handles attributes safely and provides better error handling.
    """

    def __init__(self, context: Context):
        self.context = context
        self.logger = safe_get_attr(context, "logger", logging.getLogger("behave.async_context"))
        self.loop = None

    def __enter__(self):
        # Safely get or create an event loop
        if (
            not safe_has_attr(self.context, "_async_test_loop")
            or safe_get_attr(self.context, "_async_test_loop") is None
            or safe_get_attr(safe_get_attr(self.context, "_async_test_loop", object()), "is_closed", lambda: True)()
        ):
            self.logger.info("Creating new event loop in context manager")
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            safe_set_attr(self.context, "_async_test_loop", self.loop)
        else:
            self.loop = safe_get_attr(self.context, "_async_test_loop")
            asyncio.set_event_loop(self.loop)

        # Set up main task if needed
        if not safe_has_attr(self.context, "_main_task"):

            async def setup_task():
                safe_set_attr(self.context, "_main_task", asyncio.current_task())

            try:
                self.loop.run_until_complete(setup_task())
            except Exception as e:
                self.logger.error(f"Error setting up main task: {e}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Don't close the loop here - it will be closed in after_scenario
        pass

    def run(self, coro):
        """Run a coroutine safely in the context's event loop.

        Args:
            coro: The coroutine to run

        Returns:
            The result of the coroutine
        """
        try:
            return self.loop.run_until_complete(coro)
        except Exception as e:
            self.logger.error(f"Error running coroutine: {e}")
            raise


async def async_schema_setup(async_adapter):
    """Set up database schema for async adapter."""
    # Use AsyncEngine.begin() for proper transaction handling
    async with async_adapter.session_manager.engine.begin() as conn:
        # Drop all tables (but only if they exist)
        await conn.run_sync(BaseEntity.metadata.drop_all)
        # Create all tables
        await conn.run_sync(BaseEntity.metadata.create_all)
