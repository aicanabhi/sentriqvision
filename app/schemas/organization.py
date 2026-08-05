"""
Organization Schemas
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import ConfigDict, EmailStr, Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Create Organization
# ==========================================================

class OrganizationCreate(BaseSchema):
    """
    Create Organization
    """

    organization_code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
    )


# ==========================================================
# Update Organization
# ==========================================================

class OrganizationUpdate(BaseSchema):
    """
    Update Organization
    """

    organization_code: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
    )


# ==========================================================
# Organization Response
# ==========================================================

class OrganizationResponse(BaseResponseSchema):
    """
    Organization Response
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    organization_code: str

    name: str

    email: EmailStr

    phone: Optional[str] = None

    # is_active: bool


# ==========================================================
# Organization List Response
# ==========================================================

class OrganizationListResponse(BaseSchema):
    """
    Organization List Response
    """

    total: int

    organizations: list[OrganizationResponse]