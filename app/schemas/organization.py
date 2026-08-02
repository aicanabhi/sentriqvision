"""
Organization Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    EmailStr,
    Field,
    HttpUrl,
)

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class OrganizationBase(BaseSchema):
    """
    Base organization schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    website: Optional[HttpUrl] = None

    address: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    country: Optional[str] = None

    postal_code: Optional[str] = None

    logo_url: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class OrganizationCreate(OrganizationBase):
    """
    Create organization.
    """

    plan_id: UUID


# ==========================================================
# Update
# ==========================================================

class OrganizationUpdate(BaseSchema):
    """
    Update organization.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = None

    website: Optional[HttpUrl] = None

    address: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    country: Optional[str] = None

    postal_code: Optional[str] = None

    logo_url: Optional[str] = None

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class OrganizationResponse(BaseResponseSchema):
    """
    Organization response.
    """

    code: str

    name: str

    email: EmailStr

    phone: Optional[str]

    website: Optional[HttpUrl]

    address: Optional[str]

    city: Optional[str]

    state: Optional[str]

    country: Optional[str]

    postal_code: Optional[str]

    logo_url: Optional[str]

    plan_id: UUID


# ==========================================================
# Details
# ==========================================================

class OrganizationDetailResponse(OrganizationResponse):
    """
    Organization details.
    """

    total_users: int = 0

    total_roles: int = 0

    total_teams: int = 0

    total_cameras: int = 0

    total_services: int = 0

    total_ai_models: int = 0

    total_alerts: int = 0

    storage_used_gb: float = 0.0


# ==========================================================
# List
# ==========================================================

class OrganizationListResponse(BaseSchema):
    """
    Organization list.
    """

    organizations: list[OrganizationResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class OrganizationFilter(BaseSchema):
    """
    Organization search filters.
    """

    search: Optional[str] = None

    country: Optional[str] = None

    state: Optional[str] = None

    city: Optional[str] = None

    plan_id: Optional[UUID] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Statistics
# ==========================================================

class OrganizationStatistics(BaseSchema):
    """
    Dashboard statistics.
    """

    users: int = 0

    cameras: int = 0

    services: int = 0

    ai_models: int = 0

    alerts: int = 0

    reports: int = 0

    detections: int = 0

    storage_used_gb: float = 0.0


# ==========================================================
# Delete
# ==========================================================

class OrganizationDeleteResponse(BaseSchema):
    """
    Delete response.
    """

    success: bool = True

    message: str = "Organization deleted successfully."


# ==========================================================
# Summary
# ==========================================================

class OrganizationSummary(BaseSchema):
    """
    Lightweight organization information.
    """

    id: UUID

    code: str

    name: str

    is_active: bool