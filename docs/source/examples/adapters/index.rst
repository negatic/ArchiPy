.. _examples_adapters:

Adapter Utilities
===============

ArchiPy provides adapters for interfacing with external systems:

.. admonition:: API Reference
   :class: note

   For complete API details, see: :ref:`api_adapters`

.. toctree::
   :maxdepth: 1
   :caption: Adapter Modules:

   orm
   redis
   email

Overview
--------

Adapters isolate your core application from external dependencies:

* **ORM Adapters**: Interfaces for database operations (SQLAlchemy)
* **Redis Adapters**: Key-value store and caching adapters
* **Email Adapters**: Email delivery interfaces

All adapters follow the ports and adapters pattern, with corresponding interfaces (ports) and implementations (adapters).
