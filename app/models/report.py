"""
Enterprise Report Model
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
# Report Type
# ==========================================================

class ReportType(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    ATTENDANCE = "ATTENDANCE"
    PPE = "PPE"
    FIRE = "FIRE"
    SMOKE = "SMOKE"
    VEHICLE = "VEHICLE"
    ANPR = "ANPR"
    PARKING = "PARKING"
    CROWD = "CROWD"
    FACE = "FACE"
    INCIDENT = "INCIDENT"
    CUSTOM = "CUSTOM"


# ==========================================================
# Report Format
# ==========================================================

class ReportFormat(str, enum.Enum):
    PDF = "PDF"
    EXCEL = "EXCEL"
    CSV = "CSV"
    JSON = "JSON"


# ==========================================================
# Report Status
# ==========================================================

class ReportStatus(str, enum.Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    READY = "READY"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"


# ==========================================================
# Report Model
# ==========================================================

class Report(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "reports"

    # ======================================================

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    generated_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    # ======================================================

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    report_type: Mapped[ReportType] = mapped_column(
        Enum(ReportType),
        nullable=False,
    )

    report_format: Mapped[ReportFormat] = mapped_column(
        Enum(ReportFormat),
        default=ReportFormat.PDF,
    )

    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus),
        default=ReportStatus.PENDING,
    )

    # ======================================================

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    # ======================================================

    total_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    page_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ======================================================

    file_path: Mapped[str | None] = mapped_column(
        Text,
    )

    download_url: Mapped[str | None] = mapped_column(
        Text,
    )

    checksum: Mapped[str | None] = mapped_column(
        String(128),
    )

    # ======================================================

    is_scheduled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    schedule_cron: Mapped[str | None] = mapped_column(
        String(100),
    )

    # ======================================================

    filters: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="reports",
    )

    creator = relationship(
        "User",
        foreign_keys=[generated_by],
    )

    # ======================================================

    @property
    def is_ready(self) -> bool:
        return self.status == ReportStatus.READY

    @property
    def can_download(self) -> bool:
        return (
            self.status == ReportStatus.READY
            and self.file_path is not None
        )

    def __repr__(self):
        return (
            f"<Report("
            f"{self.title}, "
            f"{self.report_type.value})>"
        )