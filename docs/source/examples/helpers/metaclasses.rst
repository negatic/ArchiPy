.. _examples_helpers_metaclasses:

Metaclasses
==========

Examples of ArchiPy's metaclass utilities:

singleton
--------

Ensure only one instance of a class exists:

.. code-block:: python

    from archipy.helpers.metaclasses.singleton import Singleton

    class ConfigManager(metaclass=Singleton):
        def __init__(self):
            self.settings = {}

        def load_config(self, path):
            # Load configuration logic
            self.settings = {"key": "value"}

    # Usage
    config1 = ConfigManager()
    config1.load_config("config.json")

    config2 = ConfigManager()
    # Both variables reference the same instance
    print(config1 is config2)  # True

    # Settings are shared
    print(config2.settings)  # {"key": "value"}
