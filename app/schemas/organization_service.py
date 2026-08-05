"""
Organization Service Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class OrganizationServiceBase(BaseSchema):
    """
    Base schema for organization services.
    """

    organization_id: UUID

    service_id: UUID

    is_enabled: bool = True

    priority: int = Field(
        default=1,
        ge=1,
        le=100,
    )

    confidence_threshold: float = Field(
        default=0.50,
        ge=0.0,
        le=1.0,
    )

    device: str = Field(
        default="AUTO",
        max_length=20,
    )

    max_fps: int = Field(
        default=15,
        ge=1,
        le=120,
    )

    schedule_enabled: bool = False

    schedule_start: Optional[str] = None

    schedule_end: Optional[str] = None

    notes: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class OrganizationServiceCreate(OrganizationServiceBase):
    """
    Enable a service for an organization.
    """

    pass


# ==========================================================
# Update
# ==========================================================

class OrganizationServiceUpdate(BaseSchema):
    """
    Update organization service configuration.
    """

    is_enabled: Optional[bool] = None

    priority: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
    )

    confidence_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    device: Optional[str] = None

    max_fps: Optional[int] = Field(
        default=None,
        ge=1,
        le=120,
    )

    schedule_enabled: Optional[bool] = None

    schedule_start: Optional[str] = None

    schedule_end: Optional[str] = None

    notes: Optional[str] = None


# ==========================================================
# Enable / Disable
# ==========================================================

class EnableOrganizationService(BaseSchema):
    """
    Enable a service.
    """

    service_id: UUID


class DisableOrganizationService(BaseSchema):
    """
    Disable a service.
    """

    service_id: UUID


# ==========================================================
# Response
# ==========================================================

class OrganizationServiceResponse(BaseResponseSchema):
    """
    Organization service response.
    """

    organization_id: UUID

    service_id: UUID

    is_enabled: bool

    priority: int

    confidence_threshold: float

    device: str

    max_fps: int

    schedule_enabled: bool

    schedule_start: Optional[str]

    schedule_end: Optional[str]

    notes: Optional[str]


# ==========================================================
# Detail Response
# ==========================================================

class OrganizationServiceDetailResponse(
    OrganizationServiceResponse
):
    """
    Detailed response.
    """

    organization_name: Optional[str] = None

    service_name: Optional[str] = None

    service_slug: Optional[str] = None


# ==========================================================
# List Response
# ==========================================================

class OrganizationServiceListResponse(BaseSchema):
    """
    Paginated service list.
    """

    services: list[OrganizationServiceResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class OrganizationServiceFilter(BaseSchema):
    """
    Search filters.
    """

    organization_id: Optional[UUID] = None

    service_id: Optional[UUID] = None

    is_enabled: Optional[bool] = None

    device: Optional[str] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Delete Response
# ==========================================================

class OrganizationServiceDeleteResponse(BaseSchema):
    """
    Delete response.
    """

    success: bool = True

    message: str = "Organization service removed successfully."