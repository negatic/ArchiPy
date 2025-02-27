.. _api_models:

Models
=====

Overview
--------

The models module contains data structures used throughout the application.


DTOs (Data Transfer Objects)
~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. automodule:: archipy.models.dtos.fastapi_exception_response_dto
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
~~~~~~~

.. automodule:: archipy.models.entities.sqlalchemy.base_entities
   :members:
   :undoc-members:
   :show-inheritance:

Errors
~~~~~

.. automodule:: archipy.models.errors.custom_errors
   :members:
   :undoc-members:
   :show-inheritance:

Types
~~~~

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
---------

Base DTOs
~~~~~~~~

.. autoclass:: archipy.models.dtos.base_dtos.BaseDTO
   :members:
   :undoc-members:
   :show-inheritance:

Base Entities
~~~~~~~~~~~

.. autoclass:: archipy.models.entities.sqlalchemy.base_entities.BaseEntity
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.entities.sqlalchemy.base_entities.UpdatableEntity
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.entities.sqlalchemy.base_entities.DeletableEntity
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.entities.sqlalchemy.base_entities.AdminEntity
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.entities.sqlalchemy.base_entities.ManagerEntity
   :members:
   :undoc-members:
   :show-inheritance:

Base Errors
~~~~~~~~~

.. autoclass:: archipy.models.errors.custom_errors.BaseError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.errors.custom_errors.NotFoundError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.errors.custom_errors.InvalidArgumentError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.errors.custom_errors.InternalError
   :members:
   :undoc-members:
   :show-inheritance:

Base Types
~~~~~~~~

.. autoclass:: archipy.models.types.base_types.BaseType
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.types.sort_order_type.SortOrderType
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: archipy.models.types.base_types.FilterOperationType
   :members:
   :undoc-members:
   :show-inheritance:
