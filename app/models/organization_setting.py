"""
Organization Settings Model

Stores organization-specific platform configuration.
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    JSON,
    String,
)



from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    ActiveMixin,
    Base,
    TimestampMixin,
    UUIDMixin,
)


class OrganizationSetting(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):

    """
    One settings record per organization.
    """

    __tablename__ = "organization_settings"


    # ==========================================================
    # Foreign Key
    # ==========================================================

    organization_id: Mapped[str] = mapped_column(
    String,
    ForeignKey(
        "organizations.id",
        ondelete="CASCADE"
    ),
    unique=True,
    nullable=False,
    index=True,
    )


    # ==========================================================
    # General Settings
    # ==========================================================

    timezone: Mapped[str] = mapped_column(
        String(100),
        default="Asia/Kolkata",
    )


    language: Mapped[str] = mapped_column(
        String(30),
        default="en",
    )


    date_format: Mapped[str] = mapped_column(
        String(30),
        default="DD-MM-YYYY",
    )


    time_format: Mapped[str] = mapped_column(
        String(10),
        default="24",
    )


    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
    )


    # ==========================================================
    # Camera Settings
    # ==========================================================

    max_cameras: Mapped[int] = mapped_column(
        Integer,
        default=50,
    )


    recording_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


    snapshot_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


    retain_video_days: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )


    retain_snapshot_days: Mapped[int] = mapped_column(
        Integer,
        default=15,
    )


    # ==========================================================
    # AI Settings
    # ==========================================================

    ai_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


    gpu_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    confidence_threshold: Mapped[int] = mapped_column(
        Integer,
        default=50,
    )


    frame_skip: Mapped[int] = mapped_column(
        Integer,
        default=2,
    )


    # ==========================================================
    # Alert Settings
    # ==========================================================

    email_alerts: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


    sms_alerts: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    whatsapp_alerts: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    webhook_alerts: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    alarm_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    # ==========================================================
    # Security
    # ==========================================================

    password_expiry_days: Mapped[int] = mapped_column(
        Integer,
        default=90,
    )


    max_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )


    session_timeout_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )


    # ==========================================================
    # Custom JSON Settings
    # ==========================================================

    extra_settings: Mapped[dict | None] = mapped_column(
        JSON,
        default=dict,
        nullable=True,
    )


    # ==========================================================
    # Relationship
    # ==========================================================

    organization = relationship(
        "Organization",
        back_populates="settings",
    )


    # ==========================================================

    def __repr__(self) -> str:

        return (
            f"<OrganizationSetting("
            f"organization_id={self.organization_id})>"
        )