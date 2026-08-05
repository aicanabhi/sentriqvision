"""
Alert Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Alert Enums
# ==========================================================

class AlertSeverity:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatus:
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# ==========================================================
# Base
# ==========================================================

class AlertBase(BaseSchema):
    """
    Base alert schema.
    """

    organization_id: UUID

    camera_id: Optional[UUID] = None

    event_id: Optional[UUID] = None

    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = None


    severity: str = Field(
        default="MEDIUM",
    )

    status: str = Field(
        default="OPEN",
    )

    source: str = Field(
        default="AI",
        max_length=50,
    )



# ==========================================================
# Create
# ==========================================================

class AlertCreate(AlertBase):
    """
    Create alert.
    """

    detection_id: Optional[UUID] = None

    confidence_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
    )

    snapshot_url: Optional[str] = None

    video_url: Optional[str] = None



# ==========================================================
# Update
# ==========================================================

class AlertUpdate(BaseSchema):
    """
    Update alert.
    """

    status: Optional[str] = None

    severity: Optional[str] = None

    assigned_to: Optional[UUID] = None

    resolution_note: Optional[str] = None



# ==========================================================
# Resolve Alert
# ==========================================================

class AlertResolveRequest(BaseSchema):
    """
    Resolve alert.
    """

    resolution_note: Optional[str] = None



# ==========================================================
# Assign Alert
# ==========================================================

class AlertAssignRequest(BaseSchema):

    user_id: UUID



# ==========================================================
# Response
# ==========================================================

class AlertResponse(BaseResponseSchema):
    """
    Alert response.
    """

    organization_id: UUID

    camera_id: Optional[UUID]

    event_id: Optional[UUID]

    detection_id: Optional[UUID]


    title: str

    description: Optional[str]


    severity: str

    status: str


    source: str


    confidence_score: Optional[float]


    snapshot_url: Optional[str]

    video_url: Optional[str]


    assigned_to: Optional[UUID]


    resolved_at: Optional[datetime]



# ==========================================================
# Detailed Response
# ==========================================================

class AlertDetailResponse(AlertResponse):
    """
    Detailed alert view.
    """

    camera_name: Optional[str] = None

    event_type: Optional[str] = None

    assigned_user_name: Optional[str] = None



# ==========================================================
# List Response
# ==========================================================

class AlertListResponse(BaseSchema):
    """
    Paginated alerts.
    """

    alerts: list[AlertResponse]

    total: int

    page: int

    page_size: int



# ==========================================================
# Filter
# ==========================================================

class AlertFilter(BaseSchema):
    """
    Alert filtering.
    """

    organization_id: Optional[UUID] = None

    camera_id: Optional[UUID] = None

    severity: Optional[str] = None

    status: Optional[str] = None

    source: Optional[str] = None


    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None


    page: int = 1

    page_size: int = 20



# ==========================================================
# Dashboard Stats
# ==========================================================

class AlertStatistics(BaseSchema):
    """
    Alert dashboard counters.
    """

    total: int = 0

    open: int = 0

    acknowledged: int = 0

    resolved: int = 0

    critical: int = 0



# ==========================================================
# Delete Response
# ==========================================================

class AlertDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Alert deleted successfully."