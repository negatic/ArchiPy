.. _examples_config:

Configuration Management Examples
================================

Basic Configuration
------------------

.. code-block:: python

    from archipy.configs.base_config import BaseConfig

    # Define a custom configuration
    class MyAppConfig(BaseConfig):
        # Override defaults
        AUTH = {
            "SECRET_KEY": "my-secure-key",
            "TOKEN_LIFETIME_MINUTES": 30
        }

        # Add custom fields
        APP_NAME = "My Application"
        DEBUG = True

    # Set as global configuration
    config = MyAppConfig()
    BaseConfig.set_global(config)

    # Access from anywhere
    from archipy.configs.base_config import BaseConfig
    current_config = BaseConfig.global_config()
    print(current_config.APP_NAME)  # "My Application"

Environment Variables
-------------------

ArchiPy configs automatically load from environment variables:

.. code-block:: bash

    # .env file
    AUTH__SECRET_KEY=production-secret-key
    AUTH__TOKEN_LIFETIME_MINUTES=15
    APP_NAME=Production App

Hierarchical Configuration
-------------------------

.. code-block:: python

    from archipy.configs.base_config import BaseConfig
    from archipy.configs.config_template import RedisConfig, SqlAlchemyConfig

    class MyAppConfig(BaseConfig):
        # Override specific Redis settings
        REDIS = RedisConfig(
            MASTER_HOST="redis.example.com",
            PORT=6380,
            PASSWORD="redis-password"
        )

        # Keep other defaults
