"""
Enterprise AI Detection Model
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    ActiveMixin,
    AuditMixin,
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)


# ==========================================================
# Detection Status
# ==========================================================

class DetectionStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DETECTED = "DETECTED"
    VERIFIED = "VERIFIED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    RESOLVED = "RESOLVED"


# ==========================================================
# Detection
# ==========================================================

class Detection(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    __tablename__ = "detections"

    # ======================================================
    # Organization
    # ======================================================

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    service_id: Mapped[str] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    camera_id: Mapped[str] = mapped_column(
        ForeignKey("cameras.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parking_zone_id: Mapped[str | None] = mapped_column(
        ForeignKey("parking_zones.id", ondelete="SET NULL"),
        nullable=True,
    )

    parking_slot_id: Mapped[str | None] = mapped_column(
        ForeignKey("parking_slots.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ======================================================
    # Detection Information
    # ======================================================

    detection_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    status: Mapped[DetectionStatus] = mapped_column(
        Enum(DetectionStatus),
        default=DetectionStatus.DETECTED,
    )

    severity: Mapped[str] = mapped_column(
        String(30),
        default="MEDIUM",
    )

    # ======================================================
    # Bounding Box
    # ======================================================

    x1: Mapped[int] = mapped_column(Integer)
    y1: Mapped[int] = mapped_column(Integer)

    x2: Mapped[int] = mapped_column(Integer)
    y2: Mapped[int] = mapped_column(Integer)

    # ======================================================
    # Tracking
    # ======================================================

    tracker_id: Mapped[int | None] = mapped_column(Integer)

    frame_number: Mapped[int | None] = mapped_column(Integer)

    frame_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    # ======================================================
    # AI Results
    # ======================================================

    ai_model: Mapped[str | None] = mapped_column(
        String(100),
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
    )

    inference_time_ms: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    # ======================================================
    # Media
    # ======================================================

    snapshot_path: Mapped[str | None] = mapped_column(
        Text,
    )

    video_clip_path: Mapped[str | None] = mapped_column(
        Text,
    )

    # ======================================================
    # Metadata
    # ======================================================

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # Example:
    # {
    #   "helmet": false,
    #   "vest": true,
    #   "plate": "UP32AB1234",
    #   "face_id": "EMP001"
    # }

    # ======================================================
    # Flags
    # ======================================================

    is_alert_generated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_notification_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship("Organization")

    service = relationship("Service")

    camera = relationship("Camera")

    parking_zone = relationship("ParkingZone")

    parking_slot = relationship("ParkingSlot")

    events = relationship(
        "Event",
        back_populates="detection",
        cascade="all, delete-orphan",
    )

    alerts = relationship(
        "Alert",
        back_populates="detection",
        cascade="all, delete-orphan",
    )

    # ======================================================

    def __repr__(self):
        return (
            f"<Detection("
            f"{self.label}, "
            f"{self.confidence:.2f})>"
        )