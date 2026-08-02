"""
Service Configuration Model

Stores runtime configuration of an AI service
for a specific organization.
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

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


class ServiceConfiguration(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    Runtime configuration for Organization AI Service.
    """

    __tablename__ = "service_configurations"

    # ======================================================
    # Foreign Key
    # ======================================================

    organization_service_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "organization_services.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    service_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "services.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ======================================================
    # AI Runtime
    # ======================================================

    confidence_threshold: Mapped[float] = mapped_column(
        Float,
        default=0.50,
    )

    iou_threshold: Mapped[float] = mapped_column(
        Float,
        default=0.45,
    )

    frame_skip: Mapped[int] = mapped_column(
        Integer,
        default=2,
    )

    max_fps: Mapped[int] = mapped_column(
        Integer,
        default=15,
    )

    batch_size: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    # ======================================================
    # Device
    # ======================================================

    device: Mapped[str] = mapped_column(
        String(20),
        default="cpu",
    )

    use_gpu: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_half_precision: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Detection
    # ======================================================

    enable_tracking: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    enable_polygon: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_roi: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_line_crossing: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Alerts
    # ======================================================

    enable_email_alert: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_sms_alert: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_whatsapp_alert: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_webhook: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_siren: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Evidence
    # ======================================================

    save_snapshot: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    save_video_clip: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    video_clip_seconds: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )

    retain_days: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    # ======================================================
    # Schedule
    # ======================================================

    schedule_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    start_time: Mapped[str | None] = mapped_column(
        String(10),
    )

    end_time: Mapped[str | None] = mapped_column(
        String(10),
    )

    # ======================================================
    # Advanced Configuration
    # ======================================================

    model_name: Mapped[str | None] = mapped_column(
        String(150),
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
    )

    custom_weights: Mapped[str | None] = mapped_column(
        String(500),
    )

    extra_config: Mapped[dict | None] = mapped_column(
        JSON,
        default=dict,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization_service = relationship(
        "OrganizationService",
        back_populates="configuration",
    )

    service = relationship(
        "Service",
        back_populates="configurations",
    )

    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<ServiceConfiguration("
            f"service='{self.service_id}', "
            f"device='{self.device}')>"
        )