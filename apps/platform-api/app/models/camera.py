import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Camera(Base):
    """
    Represents a physical CCTV camera registered in SentriqVision.
    A camera belongs to a site and can optionally belong to a zone.
    """
    __tablename__ = "cameras"
    __table_args__ = {"schema": "platform"}

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    site_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.sites.id"),
        nullable=False,
        index=True,
    )

    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.zones.id"),
        nullable=True,
        index=True,
    )

    #Human-readable camera identifier.
    camera_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    #RTSP URL will be stored securely later.
    rtsp_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    resolution: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="1080p",
    )

    fps: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=25,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="OFFLINE",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    site = relationship(
        "Site",
        back_populates="cameras"
    )

    zone = relationship(
        "Zone",
    )

    modules = relationship(
        "CameraModule",
        back_populates="camera",
        cascade="all, delete-orphan",
    )
