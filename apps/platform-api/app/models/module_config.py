import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ModuleConfig(Base):
    """
    Stores configuration for a specific camera/module combination.
    Example:
        Camera 001 + PPE
        {
        "helmet_required": true,
        "vest_required": true,
        "confidence_threshold": 0.80
        }
    """
    __tablename__ = 'module_configs'
    __table_args__ = {"schema": "platform"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    camera_module_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('platform.camera_modules.id'),
        nullable=False,
        unique=True,
    )

    #Module-specific configuration
    configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
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

    camera_module = relationship("CameraModule",)