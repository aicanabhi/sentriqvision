"""
Permission Schemas
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class PermissionBase(BaseSchema):
    """
    Base permission schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    module: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    action: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    description: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class PermissionCreate(PermissionBase):
    """
    Create permission.
    """

    pass


# ==========================================================
# Update
# ==========================================================

class PermissionUpdate(BaseSchema):
    """
    Update permission.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class PermissionResponse(BaseResponseSchema):
    """
    Permission response.
    """

    code: str

    name: str

    module: str

    action: str

    description: Optional[str]


# ==========================================================
# Summary
# ==========================================================

class PermissionSummary(BaseSchema):
    """
    Lightweight permission information.
    """

    id: UUID

    code: str

    name: str


# ==========================================================
# List Response
# ==========================================================

class PermissionListResponse(BaseSchema):
    """
    Paginated permission list.
    """

    permissions: list[PermissionResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class PermissionFilter(BaseSchema):
    """
    Search/filter permissions.
    """

    search: Optional[str] = None

    module: Optional[str] = None

    action: Optional[str] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Delete Response
# ==========================================================

class PermissionDeleteResponse(BaseSchema):
    """
    Delete response.
    """

    success: bool = True

    message: str = "Permission deleted successfully."