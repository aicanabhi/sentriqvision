"""
Role Schemas
"""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema
from app.schemas.permission import PermissionSummary


# ==========================================================
# Base
# ==========================================================

class RoleBase(BaseSchema):
    """
    Base role schema.
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

    description: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class RoleCreate(RoleBase):
    """
    Create new role.
    """

    organization_id: Optional[UUID] = None

    permission_ids: List[UUID] = []


# ==========================================================
# Update
# ==========================================================

class RoleUpdate(BaseSchema):
    """
    Update role.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    permission_ids: Optional[List[UUID]] = None

    is_active: Optional[bool] = None


# ==========================================================
# Assign Permission
# ==========================================================

class AssignPermissionRequest(BaseSchema):
    """
    Add permissions to role.
    """

    permission_ids: List[UUID]


# ==========================================================
# Remove Permission
# ==========================================================

class RemovePermissionRequest(BaseSchema):
    """
    Remove permissions from role.
    """

    permission_ids: List[UUID]


# ==========================================================
# Response
# ==========================================================

class RoleResponse(BaseResponseSchema):
    """
    Role response.
    """

    organization_id: Optional[UUID]

    name: str

    code: str

    description: Optional[str]

    permissions: List[PermissionSummary] = []


# ==========================================================
# Role Detail
# ==========================================================

class RoleDetailResponse(RoleResponse):
    """
    Detailed role information.
    """

    total_users: int = 0

    total_permissions: int = 0


# ==========================================================
# List Response
# ==========================================================

class RoleListResponse(BaseSchema):
    """
    Paginated roles.
    """

    roles: List[RoleResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class RoleFilter(BaseSchema):
    """
    Role filtering.
    """

    search: Optional[str] = None

    organization_id: Optional[UUID] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Delete Response
# ==========================================================

class RoleDeleteResponse(BaseSchema):
    """
    Delete response.
    """

    success: bool = True

    message: str = "Role deleted successfully."


# ==========================================================
# Role Summary
# ==========================================================

class RoleSummary(BaseSchema):
    """
    Lightweight role information.
    """

    id: UUID

    name: str

    code: str