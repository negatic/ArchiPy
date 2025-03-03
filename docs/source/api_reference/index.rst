.. _api_reference:

API Reference
=============

This section provides detailed documentation for all modules, classes, and functions in ArchiPy.

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   adapters
   configs
   helpers
   models

Overview
--------

ArchiPy is organized into five main modules, each serving a specific purpose in creating structured, maintainable Python applications:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Adapters
        :link: adapters
        :link-type: doc
        :img-top: ../assets/icons/adapters.svg
        :class-card: sd-rounded-3

        **Connects your core application to external systems**

        Standardized interfaces for databases, caching, messaging, and other external services with built-in testing mocks.

    .. grid-item-card:: Configs
        :link: configs
        :link-type: doc
        :img-top: ../assets/icons/config.svg
        :class-card: sd-rounded-3

        **Manages application configuration**

        Type-safe configuration management with hierarchical settings, environment variable support, and validation.

    .. grid-item-card:: Helpers
        :link: helpers
        :link-type: doc
        :img-top: ../assets/icons/helpers.svg
        :class-card: sd-rounded-3

        **Simplifies common tasks**

        Decorators, metaclasses, and utilities for retry logic, rate limiting, singleton patterns, and more.

    .. grid-item-card:: Models
        :link: models
        :link-type: doc
        :img-top: ../assets/icons/models.svg
        :class-card: sd-rounded-3

        **Standardizes data structures**

        Base classes for entities, DTOs, custom errors, and other domain objects with validation support.

Core Design Principles
---------------------

.. tab-set::

    .. tab-item:: Standardization

        ArchiPy enforces consistent patterns across your application:

        * Common base classes for entities and DTOs
        * Standardized error handling and reporting
        * Uniform configuration management
        * Consistent interface design

    .. tab-item:: Testability

        Built with testing in mind:

        * Mock implementations for all adapters
        * BDD testing support with Behave
        * Isolated test contexts
        * Dependency injection-friendly design

    .. tab-item:: Flexibility

        Works with various architectural styles:

        * Layered Architecture
        * Clean Architecture
        * Hexagonal Architecture (Ports & Adapters)
        * Domain-Driven Design
        * Service-Oriented Architecture

    .. tab-item:: Performance

        Optimized for modern Python applications:

        * Async support throughout
        * Connection pooling
        * Caching utilities
        * Efficient data handling

Quick Reference Guide
-------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Common Task
     - ArchiPy Solution
   * - Database operations
     - :class:`archipy.adapters.orm.sqlalchemy.sqlalchemy_adapters.SqlAlchemyAdapter`
   * - Caching
     - :class:`archipy.adapters.redis.redis_adapters.RedisAdapter`
   * - Configuration
     - :class:`archipy.configs.base_config.BaseConfig`
   * - Retrying operations
     - :func:`archipy.helpers.decorators.retry.retry`
   * - Date/time handling
     - :func:`archipy.helpers.utils.datetime_utils.get_utc_now`
   * - Defining entities
     - :class:`archipy.models.entities.sqlalchemy.base_entities.BaseEntity`
   * - Creating DTOs
     - :class:`archipy.models.dtos.base_dtos.BaseDTO`
   * - Password management
     - :mod:`archipy.helpers.utils.password_utils`
   * - Transaction management
     - :func:`archipy.helpers.utils.atomic_transaction.atomic_transaction`
   * - Rate limiting
     - :class:`archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler.FastAPIRestRateLimitHandler`

Module Relationships
------------------

The diagram below illustrates how ArchiPy's modules interact with each other and your application code:

.. figure:: ../assets/api_reference_diagram.png
   :alt: ArchiPy Module Relationships
   :align: center
   :width: 80%

   ArchiPy modules work together to provide a complete architecture framework
