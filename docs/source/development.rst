.. _development:

Development
==========

Development Environment
---------------------

Setting Up the Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/SyntaxArc/ArchiPy.git
      cd ArchiPy

2. Set up the project:

   .. code-block:: bash

      make setup

3. Install dependencies:

   .. code-block:: bash

      make install

4. Install development dependencies:

   .. code-block:: bash

      make install-dev

5. Install pre-commit hooks:

   .. code-block:: bash

      poetry run pre-commit install

Development Workflow
------------------

Code Quality
~~~~~~~~~~

Run all code quality checks:

.. code-block:: bash

   make check

This will run:

- **Linters**: ruff for linting
- **Formatters**: black for code formatting
- **Type Checkers**: mypy for static type checking

Testing
~~~~~~

Run tests:

.. code-block:: bash

   make test

Run BDD tests:

.. code-block:: bash

   make behave

Run the full CI pipeline locally:

.. code-block:: bash

   make ci

Pre-commit Hooks
--------------

ArchiPy uses pre-commit hooks to ensure code quality before commits. These hooks run:

- **Black**: For code formatting
- **Ruff**: For linting
- **Mypy**: For type checking
- **Additional Checks**: Various other code quality checks

To run pre-commit hooks manually:

.. code-block:: bash

   poetry run pre-commit run --all-files

Making Changes
------------

1. Create a new branch:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and ensure all tests pass:

   .. code-block:: bash

      make check
      make test

3. Commit your changes using conventional commit messages:

   .. code-block:: bash

      git commit -m "feat: add new feature"

   Common prefixes:

   - ``feat``: New feature
   - ``fix``: Bug fix
   - ``docs``: Documentation changes
   - ``style``: Formatting changes
   - ``refactor``: Code refactoring
   - ``test``: Adding or modifying tests
   - ``chore``: Maintenance tasks

4. Push your changes:

   .. code-block:: bash

      git push origin feature/your-feature-name

5. Create a pull request on GitHub

Versioning
---------

ArchiPy follows `Semantic Versioning (SemVer) <https://semver.org/>`_ principles.

Version Bumping Commands:

- Bump Patch Version (Bug fixes):

  .. code-block:: bash

     make bump-patch

- Bump Minor Version (New features):

  .. code-block:: bash

     make bump-minor

- Bump Major Version (Breaking changes):

  .. code-block:: bash

     make bump-major

Custom Version Messages:

.. code-block:: bash

   make bump-patch message="Your custom message"

Build and Distribution
--------------------

Build the package:

.. code-block:: bash

   make build

This will create:

- A wheel file (.whl)
- A source distribution (.tar.gz)

Clean build artifacts:

.. code-block:: bash

   make clean

Documentation
-----------

Build the documentation:

.. code-block:: bash

   cd docs
   make html

This will generate HTML documentation in the ``docs/build/html`` directory.

Updating Dependencies
-------------------

Update dependencies:

.. code-block:: bash

   make update

This will update all dependencies to their latest compatible versions according to the constraints in ``pyproject.toml``.
