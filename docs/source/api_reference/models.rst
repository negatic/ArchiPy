.. _api_models:

Models
======

Overview
--------

The models module standardizes data structures with base entities, DTOs, errors, and types, ensuring consistency across the application.

DTOs (Data Transfer Objects)
---------------------------

.. admonition:: Example Usage
   :class: tip

   See the :ref:`examples_helpers_utils` section for examples of using DTOs with utilities.

.. automodule:: archipy.models.dtos.base_dtos
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.dtos.email_dtos
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.dtos.error_dto
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.dtos.pagination_dto
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.dtos.range_dtos
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.dtos.search_input_dto
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.dtos.sort_dto
   :members:
   :undoc-members:
   :show-inheritance:

Entities
--------

.. automodule:: archipy.models.entities.sqlalchemy.base_entities
   :members:
   :undoc-members:
   :show-inheritance:

Errors
------

.. automodule:: archipy.models.errors.custom_errors
   :members:
   :undoc-members:
   :show-inheritance:

Types
-----

.. automodule:: archipy.models.types.base_types
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.types.email_types
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.types.exception_message_types
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.types.language_type
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: archipy.models.types.sort_order_type
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
-----------

BaseDTO
~~~~~~~

.. autoclass:: archipy.models.dtos.base_dtos.BaseDTO
   :members:
   :undoc-members:
   :show-inheritance:

BaseEntity
~~~~~~~~~~

.. autoclass:: archipy.models.entities.sqlalchemy.base_entities.BaseEntity
   :members:
   :undoc-members:
   :show-inheritance:

BaseError
~~~~~~~~~

.. autoclass:: archipy.models.errors.custom_errors.BaseError
   :members:
   :undoc-members:
   :show-inheritance:
