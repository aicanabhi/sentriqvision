import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AIParameterCatalog(Base):
    __tablename__ = "ai_parameter_catalog"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    service_number: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    domain: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hardware_requirement: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="GPU",
    )

    processing_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Real-time",
    )

    default_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.65,
    )

    default_fps: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=10.0,
    )

    configuration_schema: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    org_parameters = relationship(
        "OrganizationAIParameter",
        back_populates="catalog_item",
        cascade="all, delete-orphan",
    )


class OrganizationAIParameter(Base):
    __tablename__ = "organization_ai_parameters"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "parameter_id",
            name="uq_org_parameter",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    parameter_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "ai_parameter_catalog.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Whether this capability is enabled for the organization.
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Whether the organization has entitlement/license for it.
    entitled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Whether configuration has been completed.
    configured: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    confidence_threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.65,
    )

    sampling_fps: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=10.0,
    )

    processing_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Real-time",
    )

    device_preference: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="GPU",
    )

    alert_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    retention_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )

    configuration_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    catalog_item = relationship(
        "AIParameterCatalog",
        back_populates="org_parameters",
    )


class ParameterCameraAssignment(Base):
    __tablename__ = "parameter_camera_assignments"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "camera_id",
            "parameter_id",
            name="uq_param_cam_assignment",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    camera_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "cameras.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    parameter_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "ai_parameter_catalog.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class AIInferenceLog(Base):
    __tablename__ = "ai_inference_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )

    camera_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
        index=True,
    )

    parameter_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    device: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="GPU",
    )

    latency_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    fps: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    result_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="SUCCESS",
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
        index=True,
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    details: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )