"""
AI Service Schemas
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class ServiceBase(BaseSchema):
    """
    Base AI Service schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    description: Optional[str] = None

    icon: Optional[str] = None

    version: Optional[str] = "1.0"


# ==========================================================
# Create
# ==========================================================

class ServiceCreate(ServiceBase):
    """
    Create AI service.
    """

    model_required: bool = True

    default_enabled: bool = False


# ==========================================================
# Update
# ==========================================================

class ServiceUpdate(BaseSchema):
    """
    Update AI service.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    icon: Optional[str] = None

    version: Optional[str] = None

    model_required: Optional[bool] = None

    default_enabled: Optional[bool] = None

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class ServiceResponse(BaseResponseSchema):
    """
    Service response.
    """

    name: str

    slug: str

    category: str

    description: Optional[str]

    icon: Optional[str]

    version: Optional[str]

    model_required: bool

    default_enabled: bool


# ==========================================================
# Service Summary
# ==========================================================

class ServiceSummary(BaseSchema):
    """
    Lightweight service data.
    """

    id: UUID

    name: str

    slug: str

    category: str


# ==========================================================
# Service List
# ==========================================================

class ServiceListResponse(BaseSchema):
    """
    Paginated services.
    """

    services: list[ServiceResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class ServiceFilter(BaseSchema):
    """
    Service search filter.
    """

    search: Optional[str] = None

    category: Optional[str] = None

    is_active: Optional[bool] = None

    model_required: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Enable/Disable
# ==========================================================

class ServiceStatusUpdate(BaseSchema):
    """
    Enable or disable service globally.
    """

    is_active: bool


# ==========================================================
# Delete Response
# ==========================================================

class ServiceDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Service deleted successfully."