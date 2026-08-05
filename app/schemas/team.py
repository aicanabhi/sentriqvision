"""
Team Schemas
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema, BaseResponseSchema


# ==========================================================
# Base
# ==========================================================

class TeamBase(BaseSchema):
    """
    Common team fields.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class TeamCreate(TeamBase):
    """
    Create team inside organization.
    """

    organization_id: UUID


# ==========================================================
# Update
# ==========================================================

class TeamUpdate(BaseSchema):
    """
    Update team details.
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

class TeamResponse(BaseResponseSchema):
    """
    Team response.
    """

    organization_id: UUID

    name: str

    description: Optional[str]

    is_active: bool

    member_count: int = 0


# ==========================================================
# Detail Response
# ==========================================================

class TeamDetailResponse(TeamResponse):
    """
    Detailed team information.
    """

    members: list[UUID] = []


# ==========================================================
# List Response
# ==========================================================

class TeamListResponse(BaseSchema):
    """
    Paginated teams.
    """

    teams: list[TeamResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class TeamFilter(BaseSchema):
    """
    Team search filters.
    """

    organization_id: Optional[UUID] = None

    search: Optional[str] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Add Member
# ==========================================================

class TeamMemberAdd(BaseSchema):
    """
    Add user to team.
    """

    user_id: UUID


# ==========================================================
# Remove Member
# ==========================================================

class TeamMemberRemove(BaseSchema):
    """
    Remove user from team.
    """

    user_id: UUID


# ==========================================================
# Delete Response
# ==========================================================

class TeamDeleteResponse(BaseSchema):
    """
    Delete response.
    """

    success: bool = True

    message: str = "Team deleted successfully."