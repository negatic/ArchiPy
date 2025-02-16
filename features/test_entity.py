import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, Synonym, mapped_column

from archipy.models.entities import BaseEntity


class TestEntity(BaseEntity):
    __tablename__ = "test_entities"

    test_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default="DEFAULT",
    )
    pk_uuid: Mapped[uuid.UUID] = Synonym("test_uuid")
