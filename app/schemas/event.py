"""
Event Schemas

AI Event / Incident tracking schemas.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class EventBase(BaseSchema):
    """
    Base event schema.
    """

    organization_id: UUID

    camera_id: UUID

    event_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    category: Optional[str] = None

    description: Optional[str] = None


    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


    severity: str = Field(
        default="medium",
        max_length=20,
    )


    metadata: Optional[Dict[str, Any]] = None



# ==========================================================
# Create Event
# ==========================================================

class EventCreate(EventBase):
    """
    Create AI event.
    """

    detection_id: Optional[UUID] = None

    ai_model_id: Optional[UUID] = None



# ==========================================================
# Update Event
# ==========================================================

class EventUpdate(BaseSchema):
    """
    Update event status/details.
    """

    severity: Optional[str] = None

    description: Optional[str] = None

    metadata: Optional[Dict[str, Any]] = None

    is_resolved: Optional[bool] = None



# ==========================================================
# Response
# ==========================================================

class EventResponse(BaseResponseSchema):
    """
    Event response.
    """

    organization_id: UUID

    camera_id: UUID

    detection_id: Optional[UUID]

    ai_model_id: Optional[UUID]


    event_type: str

    category: Optional[str]

    description: Optional[str]


    confidence: float

    severity: str


    metadata: Optional[Dict[str, Any]]


    is_resolved: bool


    resolved_at: Optional[datetime]



# ==========================================================
# Detailed Event
# ==========================================================

class EventDetailResponse(EventResponse):
    """
    Detailed event information.
    """

    camera_name: Optional[str] = None

    camera_location: Optional[str] = None

    ai_model_name: Optional[str] = None

    organization_name: Optional[str] = None



# ==========================================================
# Event Filter
# ==========================================================

class EventFilter(BaseSchema):
    """
    Event searching/filtering.
    """

    organization_id: Optional[UUID] = None

    camera_id: Optional[UUID] = None

    ai_model_id: Optional[UUID] = None


    event_type: Optional[str] = None

    category: Optional[str] = None

    severity: Optional[str] = None


    is_resolved: Optional[bool] = None


    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None


    min_confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
    )


    page: int = 1

    page_size: int = 20



# ==========================================================
# List Response
# ==========================================================

class EventListResponse(BaseSchema):
    """
    Paginated events.
    """

    events: list[EventResponse]

    total: int

    page: int

    page_size: int



# ==========================================================
# Resolve Event
# ==========================================================

class EventResolveRequest(BaseSchema):
    """
    Resolve AI event.
    """

    note: Optional[str] = None



class EventResolveResponse(BaseSchema):
    """
    Resolve response.
    """

    success: bool = True

    message: str = "Event resolved successfully."