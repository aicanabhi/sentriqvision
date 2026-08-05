"""
Enterprise AI Event Model
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
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
# Event Severity
# ==========================================================

class EventSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ==========================================================
# Event Status
# ==========================================================

class EventStatus(str, enum.Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# ==========================================================
# Event Model
# ==========================================================

class Event(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "events"

    # ======================================================
    # Foreign Keys
    # ======================================================

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    detection_id: Mapped[str] = mapped_column(
        ForeignKey("detections.id", ondelete="CASCADE"),
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

    # ======================================================
    # Event Information
    # ======================================================

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    severity: Mapped[EventSeverity] = mapped_column(
        Enum(EventSeverity),
        default=EventSeverity.MEDIUM,
    )

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus),
        default=EventStatus.OPEN,
    )

    # ======================================================
    # Time
    # ======================================================

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    # ======================================================
    # User Actions
    # ======================================================

    acknowledged_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    resolved_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    # ======================================================
    # Event Source
    # ======================================================

    source: Mapped[str] = mapped_column(
        String(100),
        default="AI_ENGINE",
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
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
    # Notification Flags
    # ======================================================

    alarm_triggered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    email_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    sms_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    whatsapp_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    webhook_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Extra Data
    # ======================================================

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="events",
    )

    detection = relationship(
        "Detection",
        back_populates="events",
    )

    service = relationship(
        "Service",
    )

    camera = relationship(
        "Camera",
    )

    acknowledged_user = relationship(
        "User",
        foreign_keys=[acknowledged_by],
    )

    resolved_user = relationship(
        "User",
        foreign_keys=[resolved_by],
    )

    alerts = relationship(
        "Alert",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    notifications = relationship(
        "Notification",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    # ======================================================

    @property
    def is_open(self) -> bool:
        return self.status == EventStatus.OPEN

    @property
    def is_resolved(self) -> bool:
        return self.status == EventStatus.RESOLVED

    def __repr__(self):
        return (
            f"<Event("
            f"{self.title}, "
            f"{self.severity.value})>"
        )