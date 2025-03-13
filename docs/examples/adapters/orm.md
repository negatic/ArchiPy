# ORM Adapter Examples

This page demonstrates how to use ArchiPy's ORM adapters with SQLAlchemy.

## Basic Usage

```python
from archipy.adapters.orm.sqlalchemy import SQLAlchemyAdapter, SQLAlchemySessionManager

# Create session manager
session_manager = SQLAlchemySessionManager(connection_string="postgresql://user:pass@localhost/db")

# Create an ORM adapter
orm_adapter = SQLAlchemyAdapter(session_manager=session_manager)

# Use the adapter for database operations
users = orm_adapter.query(User).filter(User.active == True).all()
```

This documentation is being migrated from Sphinx to MkDocs format.
Please check back soon for complete content.
