.. _development:

Development
==========

Development Environment
-----------------------

Set Up
~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/SyntaxArc/ArchiPy.git
      cd ArchiPy

2. Initialize the project:

   .. code-block:: bash

      make setup

3. Install dependencies:

   .. code-block:: bash

      make install
      make install-dev  # For dev tools
      poetry run pre-commit install

Workflow
--------

Code Quality
~~~~~~~~~~~~

Run checks:

.. code-block:: bash

   make check  # Runs ruff, black, mypy

Testing
~~~~~~~

Run tests:

.. code-block:: bash

   make behave    # BDD tests
   make ci        # Full pipeline

BDD tests use `behave` with feature files in `features/` and steps in `features/steps/`.

Versioning
----------

Follow `Semantic Versioning <https://semver.org/>`_:

.. code-block:: bash

   make bump-patch  # Bug fixes
   make bump-minor  # New features
   make bump-major  # Breaking changes

Add a message:

.. code-block:: bash

   make bump-minor message="Added new utility"

Build & Docs
------------

Build the package:

.. code-block:: bash

   make build
   make clean  # Remove artifacts

Build docs:

.. code-block:: bash

   cd docs
   make html

Update dependencies:

.. code-block:: bash

   make update
