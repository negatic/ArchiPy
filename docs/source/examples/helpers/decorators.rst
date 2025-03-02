.. _examples_helpers_decorators:

Decorators
=========

Examples of ArchiPy's decorator utilities:

retry
-----

Automatically retry functions that might fail temporarily:

.. code-block:: python

    from archipy.helpers.decorators.retry import retry
    import requests

    # Retry up to 3 times with exponential backoff
    @retry(max_attempts=3, backoff_factor=2)
    def fetch_data(url):
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    try:
        data = fetch_data("https://api.example.com/data")
    except Exception as e:
        print(f"Failed after retries: {e}")

rate_limit
---------

Control the frequency of function calls:

.. code-block:: python

    from archipy.helpers.decorators.rate_limit import rate_limit

    # Limit to 5 calls per minute
    @rate_limit(max_calls=5, period=60)
    def send_notification(user_id, message):
        # Send notification logic
        print(f"Sent to {user_id}: {message}")

    # Will automatically throttle if called too frequently
    for i in range(10):
        send_notification(f"user_{i}", "Important update!")

deprecation_exception
-------------------

Mark functions as deprecated:

.. code-block:: python

    from archipy.helpers.decorators.deprecation_exception import method_deprecation_error, class_deprecation_error

    # Method deprecation
    @method_deprecation_error(operation="get_user_by_username", lang="en")
    def get_user_by_username(username):
        # This will raise a DeprecationError when called
        pass

    # Class deprecation
    @class_deprecation_error(lang="en")
    class OldUserService:
        # Using this class will raise a DeprecationError
        pass
