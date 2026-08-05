"""
Camera Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, HttpUrl

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class CameraBase(BaseSchema):
    """
    Base camera information.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = None

    location: Optional[str] = None

    ip_address: Optional[str] = None

    port: Optional[int] = Field(
        default=554,
        ge=1,
        le=65535,
    )

    manufacturer: Optional[str] = None

    model: Optional[str] = None

    serial_number: Optional[str] = None


# ==========================================================
# Create Camera
# ==========================================================

class CameraCreate(CameraBase):
    """
    Register new camera.
    """

    organization_id: UUID

    camera_group_id: Optional[UUID] = None


    # Stream

    rtsp_url: Optional[str] = None

    username: Optional[str] = None

    password: Optional[str] = None


    # Video Configuration

    resolution: Optional[str] = "1920x1080"

    fps: int = Field(
        default=25,
        ge=1,
        le=120,
    )

    codec: Optional[str] = "H264"


    # AI

    ai_enabled: bool = True

    detection_enabled: bool = True


# ==========================================================
# Update Camera
# ==========================================================

class CameraUpdate(BaseSchema):
    """
    Update camera information.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = None

    location: Optional[str] = None


    camera_group_id: Optional[UUID] = None


    rtsp_url: Optional[str] = None

    username: Optional[str] = None

    password: Optional[str] = None


    resolution: Optional[str] = None

    fps: Optional[int] = Field(
        default=None,
        ge=1,
        le=120,
    )


    ai_enabled: Optional[bool] = None

    detection_enabled: Optional[bool] = None


    is_active: Optional[bool] = None



# ==========================================================
# Stream Configuration
# ==========================================================

class CameraStreamConfig(BaseSchema):
    """
    Camera stream settings.
    """

    rtsp_url: str

    username: Optional[str] = None

    password: Optional[str] = None

    fps: int = 25

    resolution: str = "1920x1080"

    reconnect_interval: int = 5



# ==========================================================
# Response
# ==========================================================

class CameraResponse(BaseResponseSchema):
    """
    Camera response.
    """

    organization_id: UUID

    camera_group_id: Optional[UUID]


    name: str

    description: Optional[str]

    location: Optional[str]


    ip_address: Optional[str]

    port: Optional[int]


    manufacturer: Optional[str]

    model: Optional[str]

    serial_number: Optional[str]


    resolution: Optional[str]

    fps: int

    codec: Optional[str]


    ai_enabled: bool

    detection_enabled: bool


    is_active: bool


# ==========================================================
# Detail Response
# ==========================================================

class CameraDetailResponse(CameraResponse):
    """
    Detailed camera information.
    """

    group_name: Optional[str] = None

    stream_status: Optional[str] = None

    last_connected: Optional[datetime] = None

    cpu_usage: Optional[float] = None

    gpu_usage: Optional[float] = None



# ==========================================================
# Camera Status
# ==========================================================

class CameraStatusResponse(BaseSchema):
    """
    Live camera health.
    """

    camera_id: UUID

    online: bool

    stream_available: bool

    last_check: datetime

    error_message: Optional[str] = None



# ==========================================================
# Camera Filter
# ==========================================================

class CameraFilter(BaseSchema):
    """
    Camera search filters.
    """

    organization_id: Optional[UUID] = None

    camera_group_id: Optional[UUID] = None


    search: Optional[str] = None


    manufacturer: Optional[str] = None


    is_active: Optional[bool] = None


    online: Optional[bool] = None


    page: int = 1

    page_size: int = 20



# ==========================================================
# Camera List
# ==========================================================

class CameraListResponse(BaseSchema):
    """
    Paginated camera list.
    """

    cameras: list[CameraResponse]

    total: int

    page: int

    page_size: int



# ==========================================================
# Delete
# ==========================================================

class CameraDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Camera deleted successfully."