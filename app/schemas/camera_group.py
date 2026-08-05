"""
Camera Group Schemas
"""

from typing import Optional
from uuid import UUID

from app.schemas.base import (
    BaseSchema,
    BaseResponseSchema,
)


# ==========================
# Create
# ==========================

class CameraGroupCreate(BaseSchema):

    name: str

    description: Optional[str] = None



# ==========================
# Update
# ==========================

class CameraGroupUpdate(BaseSchema):

    name: Optional[str] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None



# ==========================
# Response
# ==========================

class CameraGroupResponse(BaseResponseSchema):

    name: str

    description: Optional[str]

    is_active: bool



# ==========================
# List Response
# ==========================

class CameraGroupListResponse(BaseSchema):

    groups: list[CameraGroupResponse]

    total: int