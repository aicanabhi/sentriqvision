"""
Notification Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Notification Types
# ==========================================================

class NotificationType:
    SYSTEM = "system"
    ALERT = "alert"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


# ==========================================================
# Base
# ==========================================================

class NotificationBase(BaseSchema):
    """
    Base notification schema.
    """

    user_id: UUID

    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
    )

    notification_type: str = Field(
        default="system",
        max_length=50,
    )

    priority: str = Field(
        default="normal",
        max_length=20,
    )

    is_read: bool = False


# ==========================================================
# Create
# ==========================================================

class NotificationCreate(NotificationBase):
    """
    Create notification.
    """

    alert_id: Optional[UUID] = None

    event_id: Optional[UUID] = None


# ==========================================================
# Update
# ==========================================================

class NotificationUpdate(BaseSchema):
    """
    Update notification.
    """

    is_read: Optional[bool] = None


# ==========================================================
# Mark Read
# ==========================================================

class MarkNotificationRead(BaseSchema):

    notification_id: UUID


# ==========================================================
# Response
# ==========================================================

class NotificationResponse(BaseResponseSchema):
    """
    Notification response.
    """

    user_id: UUID

    alert_id: Optional[UUID]

    event_id: Optional[UUID]

    title: str

    message: str

    notification_type: str

    priority: str

    is_read: bool

    read_at: Optional[datetime]


# ==========================================================
# Detail Response
# ==========================================================

class NotificationDetailResponse(
    NotificationResponse
):
    """
    Detailed notification.
    """

    user_name: Optional[str] = None

    organization_name: Optional[str] = None


# ==========================================================
# List Response
# ==========================================================

class NotificationListResponse(BaseSchema):
    """
    Notification list.
    """

    notifications: list[NotificationResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class NotificationFilter(BaseSchema):
    """
    Notification filters.
    """

    user_id: Optional[UUID] = None

    organization_id: Optional[UUID] = None

    notification_type: Optional[str] = None

    priority: Optional[str] = None

    is_read: Optional[bool] = None

    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Bulk Actions
# ==========================================================

class BulkNotificationRead(BaseSchema):
    """
    Mark multiple notifications as read.
    """

    notification_ids: list[UUID]


# ==========================================================
# Delete Response
# ==========================================================

class NotificationDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Notification deleted successfully."