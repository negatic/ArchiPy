.. _api_adapters:

Adapters
=======

Overview
--------

The adapters module contains implementations of ports that connect the application to external systems.

Modules
------

ORM Adapters (SQLAlchemy)
~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~

.. automodule:: archipy.adapters.redis.redis_adapters
   :members:
   :undoc-members:
   :show-inheritance:

Email Adapters
~~~~~~~~~~~~

.. automodule:: archipy.adapters.email.email_adapter
   :members:
   :undoc-members:
   :show-inheritance:

Ports
----

ORM Ports
~~~~~~~~

.. automodule:: archipy.adapters.orm.sqlalchemy.sqlalchemy_ports
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.adapters.orm.sqlalchemy.session_manager_ports
   :members:
   :undoc-members:
   :show-inheritance:

Redis Ports
~~~~~~~~~

.. automodule:: archipy.adapters.redis.redis_ports
   :members:
   :undoc-members:
   :show-inheritance:

Email Ports
~~~~~~~~~

.. automodule:: archipy.adapters.email.email_port
   :members:
   :undoc-members:
   :show-inheritance:

SQLAlchemy Adapter Classes
------------------------

SqlAlchemyAdapter
~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.SqlAlchemyAdapter
   :members:
   :undoc-members:
   :show-inheritance:

AsyncSqlAlchemyAdapter
~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.AsyncSqlAlchemyAdapter
   :members:
   :undoc-members:
   :show-inheritance:

SessionManagerAdapter
~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.session_manager_adapters.SessionManagerAdapter
   :members:
   :undoc-members:
   :show-inheritance:

AsyncSessionManagerAdapter
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.orm.sqlalchemy.session_manager_adapters.AsyncSessionManagerAdapter
   :members:
   :undoc-members:
   :show-inheritance:

Redis Adapter Classes
------------------

RedisAdapter
~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_adapters.RedisAdapter
   :members:
   :undoc-members:
   :show-inheritance:

AsyncRedisAdapter
~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.redis.redis_adapters.AsyncRedisAdapter
   :members:
   :undoc-members:
   :show-inheritance:

Email Adapter Classes
------------------

EmailAdapter
~~~~~~~~~~

.. autoclass:: archipy.adapters.email.email_adapter.EmailAdapter
   :members:
   :undoc-members:
   :show-inheritance:

EmailConnectionManager
~~~~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.email.email_adapter.EmailConnectionManager
   :members:
   :undoc-members:
   :show-inheritance:

EmailConnectionPool
~~~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.email.email_adapter.EmailConnectionPool
   :members:
   :undoc-members:
   :show-inheritance:

AttachmentHandler
~~~~~~~~~~~~~~

.. autoclass:: archipy.adapters.email.email_adapter.AttachmentHandler
   :members:
   :undoc-members:
   :show-inheritance:
