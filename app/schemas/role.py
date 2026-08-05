"""
Role Schemas
"""

from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.base import (
    BaseSchema,
    BaseResponseSchema,
)


# ==========================================================
# Base
# ==========================================================

class RoleBase(BaseSchema):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    display_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: str | None = None


# ==========================================================
# Create
# ==========================================================

class RoleCreate(RoleBase):

    organization_id: UUID | None = None


# ==========================================================
# Update
# ==========================================================

class RoleUpdate(BaseSchema):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    display_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = None

    is_active: bool | None = None


# ==========================================================
# Response
# ==========================================================

class RoleResponse(BaseResponseSchema):

    organization_id: UUID | None

    name: str

    display_name: str

    description: str | None


# ==========================================================
# List Response
# ==========================================================

class RoleListResponse(BaseSchema):

    roles: list[RoleResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Delete Response
# ==========================================================

class RoleDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Role deleted successfully."


# ==========================================================
# Role Summary
# ==========================================================

class RoleSummary(BaseSchema):

    id: UUID

    name: str

    display_name: str

    description: str | None