.. _examples_helpers:

Helper Utilities
===============

ArchiPy provides various helper utilities organized by module:

.. toctree::
   :maxdepth: 1
   :caption: Helper Modules:

   decorators
   utils
   metaclasses
   interceptors

Overview
--------

Helpers are organized into four main categories:

* **Decorators**: Function and class decorators for cross-cutting concerns
* **Utilities**: Common utility functions for routine tasks
* **Metaclasses**: Reusable class patterns through metaclasses
* **Interceptors**: Middleware components for request processing

Quick Examples
-------------

.. code-block:: python

    # Retry pattern for resilient operations
    from archipy.helpers.decorators.retry import retry

    @retry(max_attempts=3)
    def fetch_external_data():
        # Will retry up to 3 times if this fails
        pass

    # Singleton pattern for global resources
    from archipy.helpers.metaclasses.singleton import Singleton

    class DatabaseConnection(metaclass=Singleton):
        # Only one instance will ever exist
        pass

    # Date/time utilities for consistent handling
    from archipy.helpers.utils.datetime_utils import get_utc_now

    timestamp = get_utc_now()  # Always UTC-aware
