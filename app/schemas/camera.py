"""
Camera Schemas
"""

from __future__ import annotations

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.models.camera import (
    CameraStatus,
    CameraType,
)

from app.schemas.base import (
    BaseResponseSchema,
    BaseSchema,
)


# ==========================================================
# Base
# ==========================================================

class CameraBase(BaseSchema):

    camera_code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = None

    location: Optional[str] = None

    ip_address: Optional[str] = None

    port: int = Field(
        default=554,
        ge=1,
        le=65535,
    )

    manufacturer: Optional[str] = None


    model_name: Optional[str] = None


    serial_number: Optional[str] = None


# ==========================================================
# Create Camera
# ==========================================================

class CameraCreate(CameraBase):

    organization_id: UUID


    ai_enabled: bool = True

    
    camera_group_id: Optional[UUID] = None
    recording_enabled: bool = True
    detection_enabled: bool = True
    alerts_enabled: bool = True


    # Connection

    rtsp_url: Optional[str] = None

    username: Optional[str] = None

    password: Optional[str] = None


    # Stream

    resolution: str = "1920x1080"

    fps: int = Field(
        default=25,
        ge=1,
        le=120,
    )

    codec: str = "H264"


    # AI

    ai_enabled: bool = True
    detection_enabled: bool = True



# ==========================================================
# Update Camera
# ==========================================================

class CameraUpdate(BaseSchema):

    name: Optional[str] = None

    description: Optional[str] = None

    location: Optional[str] = None

    ip_address: Optional[str] = None

    port: Optional[int] = None


    camera_group_id: Optional[UUID] = None


    rtsp_url: Optional[str] = None

    username: Optional[str] = None

    password: Optional[str] = None


    resolution: Optional[str] = None

    fps: Optional[int] = None

    codec: Optional[str] = None


    ai_enabled: Optional[bool] = None

    recording_enabled: Optional[bool] = None

    detection_enabled: Optional[bool] = None

    alerts_enabled: Optional[bool] = None

    is_active: Optional[bool] = None



# ==========================================================
# Response
# ==========================================================

class CameraResponse(BaseResponseSchema):

    organization_id: UUID

    camera_group_id: Optional[UUID]


    camera_code: str

    name: str

    description: Optional[str]

    location: Optional[str]


    ip_address: Optional[str]

    port: int


    rtsp_url: Optional[str]

    username: Optional[str]


    resolution: Optional[str]

    fps: int

    codec: Optional[str]


    camera_type: CameraType

    status: CameraStatus


    ai_enabled: bool

    recording_enabled: bool

    detection_enabled: bool

    alerts_enabled: bool



# ==========================================================
# Detail Response
# ==========================================================

class CameraDetailResponse(CameraResponse):

    manufacturer: Optional[str]

    model_name: Optional[str]

    serial_number: Optional[str]

    firmware_version: Optional[str]


    building: Optional[str]

    floor: Optional[str]

    zone: Optional[str]


    snapshot_url: Optional[str]

    onvif_url: Optional[str]


    bitrate: Optional[int]


    latitude: Optional[float]

    longitude: Optional[float]


    last_seen: Optional[str]



# ==========================================================
# Status Response
# ==========================================================

class CameraStatusResponse(BaseSchema):

    camera_id: UUID

    status: CameraStatus

    is_active: bool

    last_seen: Optional[str]



# ==========================================================
# List Response
# ==========================================================

class CameraListResponse(BaseSchema):

    cameras: list[CameraResponse]

    total: int

    page: int

    page_size: int



# ==========================================================
# Delete Response
# ==========================================================

class CameraDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Camera deleted successfully."