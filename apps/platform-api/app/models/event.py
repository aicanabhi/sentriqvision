import uuid
from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Event(Base):
    """
    Represents a meaningful AI-detected incident.
    Examples:
        HELMET_MISSING
        FIRE_DETECTED
        INTRUSION
        CROWD_DETECTED
    """

    __tablename__ = "events"
    __table_args__ = {"schema": "platform"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    camera_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.cameras.id"),
        nullable=False,
        index=True,
    )

    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.zones.id"),
        nullable=False,
        index=True,
    )

    module_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.modules.id"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    condition_id: Mapped[Float] = mapped_column(
        Float,
        nullable=False,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    event_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    camera = relationship("Camera")
    zone = relationship("Zone")
    module = relationship("Module")