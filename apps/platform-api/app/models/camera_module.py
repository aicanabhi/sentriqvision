import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class CameraModule(Base):
    """
    Connects a camera to an AI module.

    This represents which AI capabilities are enabled for a particular camera.
    """

    __tablename__ = "camera_modules"
    __table_args__ = (
        UniqueConstraint("camera_id", "module_id",
                         name="uq_camera_module",
                         ),
        {"schema": "platform"},
        )

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

    module_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.modules.id"),
        nullable=False,
        index=True,
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    camera = relationship("Camera", back_populates="modules")
    module = relationship("Module",)
