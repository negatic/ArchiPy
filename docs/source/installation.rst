.. _installation:

Installation
===========

Prerequisites
------------

Before you begin, ensure you have the following installed:

- **Python 3.13 or higher**

  ArchiPy is compatible with Python 3.13 and above but does not support Python 4 or higher.
  To check your Python version, run:

  .. code-block:: bash

     python --version

  If your Python version is lower than 3.13, `download and install the latest version of Python <https://www.python.org/downloads/>`_.

- **Poetry** (for dependency management)

  Poetry is required to manage dependencies and install the project. If you don't have Poetry installed, follow the `official installation guide <https://python-poetry.org/docs/>`_.

Installation Methods
-------------------

Using pip
~~~~~~~~~

To install the core library:

.. code-block:: bash

   pip install archipy

To install the library with optional dependencies (e.g., ``redis``, ``fastapi``, etc.):

.. code-block:: bash

   pip install archipy[redis,fastapi]

Using poetry
~~~~~~~~~~~

To add the core library to your project:

.. code-block:: bash

   poetry add archipy

To add the library with optional dependencies (e.g., ``redis``, ``fastapi``, etc.):

.. code-block:: bash

   poetry add archipy[redis,fastapi]

Optional Dependencies
-------------------

The library provides optional dependencies for additional functionality. You can install them as needed:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - Installation Command
   * - Redis
     - ``archipy[redis]``
   * - Elastic APM
     - ``archipy[elastic-apm]``
   * - FastAPI
     - ``archipy[fastapi]``
   * - JWT
     - ``archipy[jwt]``
   * - Kavenegar
     - ``archipy[kavenegar]``
   * - Prometheus
     - ``archipy[prometheus]``
   * - Sentry
     - ``archipy[sentry]``
   * - Dependency Injection
     - ``archipy[dependency-injection]``
   * - Scheduler
     - ``archipy[scheduler]``
   * - gRPC
     - ``archipy[grpc]``
   * - PostgreSQL
     - ``archipy[postgres]``
   * - aiosqlite
     - ``archipy[aiosqlite]``

Development Installation
-----------------------

For contributors and developers:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/SyntaxArc/ArchiPy.git
   cd ArchiPy

   # Set up the project
   make setup

   # Install dependencies
   make install

   # Install development dependencies (optional)
   make install-dev

Troubleshooting Installation Issues
----------------------------------

If you encounter issues during installation, ensure that:

1. Your Python version is **3.13 or higher**.
2. Your package manager (``pip`` or ``poetry``) is up to date.
3. You have the necessary build tools installed (e.g., ``setuptools``, ``wheel``).

For example, to upgrade ``pip``, run:

.. code-block:: bash

   pip install --upgrade pip
