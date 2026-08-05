"""
Enterprise Camera Model
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import (
    ActiveMixin,
    AuditMixin,
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)


# ============================================================
# Camera Status
# ============================================================

class CameraStatus(str, enum.Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    CONNECTING = "CONNECTING"
    ERROR = "ERROR"
    DISABLED = "DISABLED"


# ============================================================
# Camera Type
# ============================================================

class CameraType(str, enum.Enum):
    IP = "IP"
    USB = "USB"
    RTSP = "RTSP"
    RTMP = "RTMP"
    HTTP = "HTTP"
    ONVIF = "ONVIF"


# ============================================================
# Camera Model
# ============================================================

class Camera(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    __tablename__ = "cameras"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "camera_code",
            name="uq_camera_code_per_org",
        ),
    )

    # ========================================================
    # Organization
    # ========================================================

    organization_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ========================================================
    # Camera Group
    # ========================================================

    camera_group_id: Mapped[str | None] = mapped_column(
        String,
        ForeignKey("camera_groups.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ========================================================
    # Team
    # ========================================================

    team_id: Mapped[str | None] = mapped_column(
        String,
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ========================================================
    # Basic Information
    # ========================================================

    camera_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text)

    location: Mapped[str | None] = mapped_column(String(255))

    building: Mapped[str | None] = mapped_column(String(100))

    floor: Mapped[str | None] = mapped_column(String(100))

    zone: Mapped[str | None] = mapped_column(String(100))

    # ========================================================
    # Camera Details
    # ========================================================

    camera_type: Mapped[CameraType] = mapped_column(
        Enum(CameraType),
        default=CameraType.RTSP,
    )

    manufacturer: Mapped[str | None] = mapped_column(String(100))

    model_name: Mapped[str | None] = mapped_column(String(100))

    serial_number: Mapped[str | None] = mapped_column(String(100))

    firmware_version: Mapped[str | None] = mapped_column(String(100))

    # ========================================================
    # Connection
    # ========================================================

    ip_address: Mapped[str | None] = mapped_column(String(50))

    port: Mapped[int] = mapped_column(
        Integer,
        default=554,
    )

    username: Mapped[str | None] = mapped_column(String(100))

    password: Mapped[str | None] = mapped_column(String(255))

    rtsp_url: Mapped[str | None] = mapped_column(Text)

    snapshot_url: Mapped[str | None] = mapped_column(Text)

    onvif_url: Mapped[str | None] = mapped_column(Text)

    # ========================================================
    # Stream
    # ========================================================

    resolution: Mapped[str | None] = mapped_column(
        String(50),
        default="1920x1080",
    )

    fps: Mapped[int] = mapped_column(
        Integer,
        default=25,
    )

    bitrate: Mapped[int | None] = mapped_column(Integer)

    codec: Mapped[str | None] = mapped_column(
        String(50),
        default="H264",
    )

    # ========================================================
    # AI Configuration
    # ========================================================

    ai_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    detection_enabled: Mapped[bool] = mapped_column(
    Boolean,
    default=True,
    )

    recording_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    alerts_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    services_enabled: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # Example:
    # {
    #   "face_recognition": true,
    #   "helmet": true,
    #   "ppe": false
    # }

    # ========================================================
    # Status
    # ========================================================

    status: Mapped[CameraStatus] = mapped_column(
        Enum(CameraStatus),
        default=CameraStatus.OFFLINE,
    )

    last_seen: Mapped[str | None] = mapped_column(String(100))

    # ========================================================
    # Geo
    # ========================================================

    latitude: Mapped[float | None] = mapped_column(Float)

    longitude: Mapped[float | None] = mapped_column(Float)

    # ========================================================
    # Relationships
    # ========================================================

    organization = relationship(
        "Organization",
        back_populates="cameras",
    )

    group = relationship(
        "CameraGroup",
        back_populates="cameras",
    )

    team = relationship(
        "Team",
    )

    health = relationship(
        "CameraHealth",
        back_populates="camera",
        uselist=False,
        cascade="all, delete-orphan",
    )

    stream = relationship(
        "CameraStream",
        back_populates="camera",
        uselist=False,
        cascade="all, delete-orphan",
    )

    detections = relationship(
        "Detection",
        back_populates="camera",
        cascade="all, delete-orphan",
    )

    alerts = relationship(
        "Alert",
        back_populates="camera",
        cascade="all, delete-orphan",
    )

    # ========================================================

    def __repr__(self) -> str:
        return (
            f"<Camera("
            f"name='{self.name}', "
            f"status='{self.status.value}')>"
        )