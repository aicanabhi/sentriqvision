"""
Enterprise Alert Model
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
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
# Alert Severity
# ==========================================================

class AlertSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ==========================================================
# Alert Status
# ==========================================================

class AlertStatus(str, enum.Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# ==========================================================
# Alert Priority
# ==========================================================

class AlertPriority(str, enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


# ==========================================================
# Alert
# ==========================================================

class Alert(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "alerts"

    # ------------------------------------------------------

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_id: Mapped[str] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    detection_id: Mapped[str] = mapped_column(
        ForeignKey("detections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    camera_id: Mapped[str] = mapped_column(
        ForeignKey("cameras.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    service_id: Mapped[str] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------

    alert_code: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity),
        default=AlertSeverity.MEDIUM,
    )

    priority: Mapped[AlertPriority] = mapped_column(
        Enum(AlertPriority),
        default=AlertPriority.P3,
    )

    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus),
        default=AlertStatus.OPEN,
    )

    # ------------------------------------------------------

    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    # ------------------------------------------------------

    assigned_to: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    acknowledged_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    resolved_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    # ------------------------------------------------------

    snapshot_path: Mapped[str | None] = mapped_column(Text)

    video_clip_path: Mapped[str | None] = mapped_column(Text)

    # ------------------------------------------------------

    alarm_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    email_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    sms_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    whatsapp_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    push_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    webhook_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    auto_close: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    auto_close_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    # ------------------------------------------------------

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="alerts",
    )

    detection = relationship(
        "Detection",
        back_populates="alerts",
    )

    event = relationship(
        "Event",
        back_populates="alerts",
    )

    service = relationship("Service")

    camera = relationship("Camera")

    assigned_user = relationship(
        "User",
        foreign_keys=[assigned_to],
    )

    acknowledged_user = relationship(
        "User",
        foreign_keys=[acknowledged_by],
    )

    resolved_user = relationship(
        "User",
        foreign_keys=[resolved_by],
    )

    notifications = relationship(
        "Notification",
        back_populates="alert",
        cascade="all, delete-orphan",
    )

    # ======================================================

    @property
    def is_open(self) -> bool:
        return self.status == AlertStatus.OPEN

    @property
    def is_closed(self) -> bool:
        return self.status == AlertStatus.CLOSED

    def __repr__(self) -> str:
        return (
            f"<Alert("
            f"{self.alert_code}, "
            f"{self.status.value})>"
        )