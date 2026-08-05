"""
AI Model Registry
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
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
# Model Status
# ==========================================================

class AIModelStatus(str, enum.Enum):
    TRAINING = "TRAINING"
    READY = "READY"
    DEPLOYED = "DEPLOYED"
    DISABLED = "DISABLED"
    ARCHIVED = "ARCHIVED"


# ==========================================================
# AI Model
# ==========================================================

class AIModel(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "ai_models"

    # -------------------------------------------------------

    organization_id: Mapped[str | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
    )

    service_id: Mapped[str] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # -------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    framework: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    task: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[AIModelStatus] = mapped_column(
        Enum(AIModelStatus),
        default=AIModelStatus.READY,
    )

    # -------------------------------------------------------

    model_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    labels_path: Mapped[str | None] = mapped_column(Text)

    config_path: Mapped[str | None] = mapped_column(Text)

    # -------------------------------------------------------

    input_width: Mapped[int] = mapped_column(default=640)

    input_height: Mapped[int] = mapped_column(default=640)

    batch_size: Mapped[int] = mapped_column(default=1)

    # -------------------------------------------------------

    confidence_threshold: Mapped[float] = mapped_column(default=0.50)

    nms_threshold: Mapped[float] = mapped_column(default=0.45)

    # -------------------------------------------------------

    device: Mapped[str] = mapped_column(
        String(20),
        default="AUTO",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # -------------------------------------------------------

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # -------------------------------------------------------

    organization = relationship(
        "Organization",
        back_populates="ai_models",
    )

    service = relationship(
        "Service",
    )

    # -------------------------------------------------------

    def __repr__(self):
        return (
            f"<AIModel("
            f"{self.name} "
            f"{self.version})>"
        )