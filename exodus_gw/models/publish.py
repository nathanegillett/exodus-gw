import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Publish(Base):

    __tablename__ = "publishes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    env = Column(String, nullable=False)
    state = Column(String, nullable=False)
    updated = Column(DateTime(timezone=True))
    items = relationship(
        "Item", back_populates="publish", cascade="all, delete-orphan"
    )


@event.listens_for(Publish, "before_update")
def publish_before_update(_mapper, _connection, publish):
    publish.updated = datetime.now(timezone.utc)


class Item(Base):

    __tablename__ = "items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    web_uri = Column(String, nullable=False)
    object_key = Column(String, nullable=False)
    publish_id = Column(
        UUID(as_uuid=True), ForeignKey("publishes.id"), nullable=False
    )

    publish = relationship("Publish", back_populates="items")
