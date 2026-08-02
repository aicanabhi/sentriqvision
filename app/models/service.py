"""
Master AI Services Model

This table contains all AI services available in the platform.
Only Super Admin can manage these services.
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Enum,
    Integer,
    String,
    Text,
)

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
# Service Category
# ==========================================================

class ServiceCategory(str, enum.Enum):
    SECURITY = "SECURITY"
    SAFETY = "SAFETY"
    PARKING = "PARKING"
    TRAFFIC = "TRAFFIC"
    OCR = "OCR"
    ATTENDANCE = "ATTENDANCE"
    ANALYTICS = "ANALYTICS"
    AI = "AI"
    OTHER = "OTHER"


# ==========================================================
# Service Model
# ==========================================================

class Service(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    Master AI Services.
    """

    __tablename__ = "services"

    # ======================================================
    # Basic Information
    # ======================================================

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    category: Mapped[ServiceCategory] = mapped_column(
        Enum(ServiceCategory),
        nullable=False,
        default=ServiceCategory.AI,
    )

    # ======================================================
    # AI Model Information
    # ======================================================

    model_name: Mapped[str | None] = mapped_column(
        String(150),
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
    )

    ai_module: Mapped[str | None] = mapped_column(
        String(200),
    )

    # Example:
    # app.ai_modules.face_recognition.main

    # ======================================================
    # Runtime Settings
    # ======================================================

    default_confidence: Mapped[int] = mapped_column(
        Integer,
        default=50,
    )

    default_frame_skip: Mapped[int] = mapped_column(
        Integer,
        default=2,
    )

    supports_gpu: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    supports_cpu: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    requires_camera: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    requires_gpu: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Licensing
    # ======================================================

    premium_service: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    visible_to_customer: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organizations = relationship(
        "OrganizationService",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    configurations = relationship(
        "ServiceConfiguration",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Service("
            f"name='{self.name}', "
            f"category='{self.category}')>"
        )