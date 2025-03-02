.. _api_adapters:

Adapters
========

Overview
--------

Adapters connect ArchiPy to external systems (e.g., databases, Redis, email) via well-defined ports. This module supports the goal of providing common adapters with mocks for delegation and testing, enabling seamless integration and isolated unit tests.

Adapters
--------

ORM Adapters (SQLAlchemy)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.adapters.orm.sqlalchemy.session_manager_adapters
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.adapters.orm.sqlalchemy.session_manager_mocks
   :members:
   :undoc-members:
   :show-inheritance:

Redis Adapters
~~~~~~~~~~~~~~

.. automodule:: archipy.adapters.redis.redis_adapters
   :members:
   :undoc-members:
   :show-inheritance:

Email Adapters
~~~~~~~~~~~~~~

.. automodule:: archipy.adapters.email.email_adapter
   :members:
   :undoc-members:
   :show-inheritance:

Ports
-----

Define interfaces for adapters, ensuring flexibility and testability.

ORM Ports
~~~~~~~~~

.. automodule:: archipy.adapters.orm.sqlalchemy.sqlalchemy_ports
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.adapters.orm.sqlalchemy.session_manager_ports
   :members:
   :undoc-members:
   :show-inheritance:

Redis Ports
~~~~~~~~~~~

.. automodule:: archipy.adapters.redis.redis_ports
   :members:
   :undoc-members:
   :show-inheritance:

Email Ports
~~~~~~~~~~~

.. automodule:: archipy.adapters.email.email_port
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
-----------

SqlAlchemyAdapter
~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.SqlAlchemyAdapter
   :members:
   :undoc-members:
   :show-inheritance:

AsyncSqlAlchemyAdapter
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.AsyncSqlAlchemyAdapter
   :members:
   :undoc-members:
   :show-inheritance:

RedisAdapter
~~~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_adapters.RedisAdapter
   :members:
   :undoc-members:
   :show-inheritance:

AsyncRedisAdapter
~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_adapters.AsyncRedisAdapter
   :members:
   :undoc-members:
   :show-inheritance:

EmailAdapter
~~~~~~~~~~~~

.. autoclass:: archipy.adapters.email.email_adapter.EmailAdapter
   :members:
   :undoc-members:
   :show-inheritance:
