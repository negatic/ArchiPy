.. _api_configs:

Configs
=======

Overview
--------

The configs module provides tools for standardized configuration management and injection, supporting consistent setup across services like databases, Redis, and email.

Configuration Classes
---------------------

Base Config
~~~~~~~~~~~

.. automodule:: archipy.configs.base_config
   :members:
   :undoc-members:
   :show-inheritance:

Config Templates
~~~~~~~~~~~~~~~~

.. automodule:: archipy.configs.config_template
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
-----------

BaseConfig
~~~~~~~~~~

.. autoclass:: archipy.configs.base_config.BaseConfig
   :members:
   :undoc-members:
   :show-inheritance:

SqlAlchemyConfig
~~~~~~~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.SqlAlchemyConfig
   :members:
   :undoc-members:
   :show-inheritance:

RedisConfig
~~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.RedisConfig
   :members:
   :undoc-members:
   :show-inheritance:

EmailConfig
~~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.EmailConfig
   :members:
   :undoc-members:
   :show-inheritance:

FastAPIConfig
~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.FastAPIConfig
   :members:
   :undoc-members:
   :show-inheritance:

GrpcConfig
~~~~~~~~

.. autoclass:: archipy.configs.config_template.GrpcConfig
   :members:
   :undoc-members:
   :show-inheritance:

SentryConfig
~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.SentryConfig
   :members:
   :undoc-members:
   :show-inheritance:

ElasticSearchConfig
~~~~~~~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.ElasticSearchConfig
   :members:
   :undoc-members:
   :show-inheritance:

ElasticSearchAPMConfig
~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.configs.config_template.ElasticSearchAPMConfig
   :members:
   :undoc-members:
   :show-inheritance:

KafkaConfig
~~~~~~~~~

.. autoclass:: archipy.configs.config_template.KafkaConfig
   :members:
   :undoc-members:
   :show-inheritance:

EnvironmentType
~~~~~~~~~~~~

.. autoclass:: archipy.configs.environment_type.EnvironmentType
   :members:
   :undoc-members:
   :show-inheritance:
