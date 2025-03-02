.. ArchiPy documentation master file

Welcome to ArchiPy
=================

.. image:: https://img.shields.io/badge/python-3.13+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.13+

.. image:: ../assets/logo.jpg
   :alt: ArchiPy Logo
   :width: 150
   :align: right

**Architecture + Python – Structured Development Simplified**

ArchiPy provides a clean architecture framework for Python applications that:

* Standardizes configuration management
* Offers pluggable adapters with testing mocks
* Enforces consistent data models
* Promotes maintainable code organization
* Simplifies testing with BDD support

.. grid:: 2

    .. grid-item-card:: 🚀 Quick Start
        :link: installation
        :link-type: ref

        Get started with ArchiPy in minutes

    .. grid-item-card:: 📚 Features
        :link: features
        :link-type: ref

        Explore what ArchiPy offers

    .. grid-item-card:: 🏗️ Architecture
        :link: architecture
        :link-type: ref

        Learn about the design principles

    .. grid-item-card:: 🔍 API Reference
        :link: api_reference/index
        :link-type: ref

        Detailed API documentation

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents:

   installation
   usage
   features
   architecture
   api_reference/index
   development
   contributing
   changelog
   license

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Examples:

   examples/config_management
   examples/adapters/index
   examples/helpers/index
   examples/bdd_testing

Quick Start
----------

.. code-block:: bash

   # Install using pip
   pip install archipy

   # Or with poetry
   poetry add archipy

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
