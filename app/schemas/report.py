"""
Report Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Report Types
# ==========================================================

REPORT_TYPES = [
    "camera",
    "detection",
    "event",
    "alert",
    "attendance",
    "parking",
    "analytics",
    "system",
]


EXPORT_FORMATS = [
    "pdf",
    "excel",
    "csv",
]


# ==========================================================
# Base
# ==========================================================

class ReportBase(BaseSchema):
    """
    Base report schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    report_type: str

    description: Optional[str] = None


# ==========================================================
# Create Report
# ==========================================================

class ReportCreate(ReportBase):
    """
    Create report configuration.
    """

    organization_id: UUID

    camera_id: Optional[UUID] = None

    user_id: Optional[UUID] = None

    export_format: str = "pdf"

    start_date: datetime

    end_date: datetime


# ==========================================================
# Generate Report Request
# ==========================================================

class ReportGenerateRequest(BaseSchema):
    """
    Generate report instantly.
    """

    organization_id: UUID

    report_type: str

    export_format: str = "pdf"

    camera_ids: Optional[list[UUID]] = None

    start_date: datetime

    end_date: datetime

    include_images: bool = False

    include_charts: bool = True


# ==========================================================
# Update Report
# ==========================================================

class ReportUpdate(BaseSchema):
    """
    Update report configuration.
    """

    name: Optional[str] = None

    description: Optional[str] = None

    export_format: Optional[str] = None

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class ReportResponse(BaseResponseSchema):
    """
    Report response.
    """

    organization_id: UUID

    name: str

    report_type: str

    description: Optional[str]

    export_format: str

    file_url: Optional[str]

    status: str

    generated_at: Optional[datetime]


# ==========================================================
# Report Detail
# ==========================================================

class ReportDetailResponse(ReportResponse):
    """
    Detailed report information.
    """

    total_events: int = 0

    total_alerts: int = 0

    total_detections: int = 0

    total_cameras: int = 0

    processing_time_seconds: Optional[float] = None


# ==========================================================
# List Response
# ==========================================================

class ReportListResponse(BaseSchema):
    """
    Paginated reports.
    """

    reports: list[ReportResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class ReportFilter(BaseSchema):
    """
    Report search filters.
    """

    organization_id: Optional[UUID] = None

    report_type: Optional[str] = None

    status: Optional[str] = None

    export_format: Optional[str] = None

    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Scheduled Report
# ==========================================================

class ScheduledReportCreate(BaseSchema):
    """
    Create scheduled reports.
    """

    organization_id: UUID

    report_type: str

    frequency: str = Field(
        default="daily"
    )

    export_format: str = "pdf"

    email_recipients: list[str]

    enabled: bool = True


# ==========================================================
# Download Response
# ==========================================================

class ReportDownloadResponse(BaseSchema):
    """
    Report download response.
    """

    file_url: str

    file_name: str

    expires_at: datetime


# ==========================================================
# Delete Response
# ==========================================================

class ReportDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Report deleted successfully."