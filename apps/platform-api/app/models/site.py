import uuid
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, String, ForeignKey, func
from .base import Base
class Site(Base):
    """
    Physical location belonging to an organization.

    Example:

        ABC Industries
        ├── Mumbai Plant
        ├── Pune Plant
        └── Delhi Warehouse
    """
    __tablename__ = "sites"
    __table_args__ = {"schema": "platform"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    #Parent organization
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.organizations.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="UTC",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ACTIVE",
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

    # Many sites belong to one organization.
    organization = relationship(
        "Organization",
        back_populates="sites",
    )

    zones = relationship(
        "Zone",
        back_populates="site",
        cascade="all, delete-orphan",
    )

    cameras = relationship(
        "Camera",
        back_populates="site",
        cascade="all, delete-orphan",
    )