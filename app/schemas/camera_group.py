"""
Camera Group Schemas
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class CameraGroupBase(BaseSchema):

    organization_id: UUID

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None

    location: Optional[str] = None

    is_active: bool = True



# ==========================================================
# Create
# ==========================================================

class CameraGroupCreate(CameraGroupBase):
    """
    Create camera group.
    """

    pass



# ==========================================================
# Update
# ==========================================================

class CameraGroupUpdate(BaseSchema):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None

    location: Optional[str] = None

    is_active: Optional[bool] = None



# ==========================================================
# Response
# ==========================================================

class CameraGroupResponse(BaseResponseSchema):

    organization_id: UUID

    name: str

    description: Optional[str]

    location: Optional[str]

    is_active: bool

    total_cameras: int = 0



# ==========================================================
# Detail Response
# ==========================================================

class CameraGroupDetailResponse(CameraGroupResponse):

    cameras: list[dict] = []



# ==========================================================
# List Response
# ==========================================================

class CameraGroupListResponse(BaseSchema):

    groups: list[CameraGroupResponse]

    total: int

    page: int

    page_size: int



# ==========================================================
# Filter
# ==========================================================

class CameraGroupFilter(BaseSchema):

    organization_id: Optional[UUID] = None

    search: Optional[str] = None

    location: Optional[str] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20



# ==========================================================
# Delete Response
# ==========================================================

class CameraGroupDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Camera group deleted successfully."