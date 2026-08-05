"""
Permission Schemas
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.models.permission import PermissionCategory
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

    display_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    category: PermissionCategory

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
    Create permission schema.
    """

    pass


# ==========================================================
# Update
# ==========================================================

class PermissionUpdate(BaseSchema):
    """
    Update permission schema.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    code: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    display_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    category: Optional[PermissionCategory] = None

    module: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    action: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    description: Optional[str] = None

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class PermissionResponse(BaseResponseSchema):
    """
    Permission response schema.
    """

    name: str

    code: str

    display_name: str

    category: PermissionCategory

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

    name: str

    code: str

    display_name: str

    category: PermissionCategory


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
    Permission search filters.
    """

    search: Optional[str] = None

    module: Optional[str] = None

    category: Optional[PermissionCategory] = None

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