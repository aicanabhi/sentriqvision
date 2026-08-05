"""
Subscription Plan Schemas
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class PlanBase(BaseSchema):
    """
    Base plan schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    description: Optional[str] = None

    price: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )

    duration_days: int = Field(
        default=30,
        ge=1,
    )

    max_users: int = Field(
        default=10,
        ge=1,
    )

    max_cameras: int = Field(
        default=10,
        ge=1,
    )

    max_storage_gb: int = Field(
        default=100,
        ge=1,
    )

    max_ai_models: int = Field(
        default=5,
        ge=1,
    )

    trial_days: int = Field(
        default=0,
        ge=0,
    )

    is_public: bool = True

    is_default: bool = False


# ==========================================================
# Create
# ==========================================================

class PlanCreate(PlanBase):
    """
    Create subscription plan.
    """

    pass


# ==========================================================
# Update
# ==========================================================

class PlanUpdate(BaseSchema):
    """
    Update subscription plan.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    price: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    duration_days: Optional[int] = Field(
        default=None,
        ge=1,
    )

    max_users: Optional[int] = Field(
        default=None,
        ge=1,
    )

    max_cameras: Optional[int] = Field(
        default=None,
        ge=1,
    )

    max_storage_gb: Optional[int] = Field(
        default=None,
        ge=1,
    )

    max_ai_models: Optional[int] = Field(
        default=None,
        ge=1,
    )

    trial_days: Optional[int] = Field(
        default=None,
        ge=0,
    )

    is_public: Optional[bool] = None

    is_default: Optional[bool] = None

    is_active: Optional[bool] = None


# ==========================================================
# Response
# ==========================================================

class PlanResponse(BaseResponseSchema):
    """
    Plan response schema.
    """

    code: str

    name: str

    description: Optional[str]

    price: Decimal

    duration_days: int

    max_users: int

    max_cameras: int

    max_storage_gb: int

    max_ai_models: int

    trial_days: int

    is_public: bool

    is_default: bool


# ==========================================================
# List Response
# ==========================================================

class PlanListResponse(BaseSchema):
    """
    Paginated plan list.
    """

    plans: list[PlanResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class PlanFilter(BaseSchema):
    """
    Plan filters.
    """

    search: Optional[str] = None

    is_active: Optional[bool] = None

    is_public: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Delete Response
# ==========================================================

class PlanDeleteResponse(BaseSchema):
    """
    Delete response.
    """

    success: bool = True

    message: str = "Plan deleted successfully."


# ==========================================================
# Plan Summary
# ==========================================================

class PlanSummary(BaseSchema):
    """
    Lightweight plan information.
    """

    id: UUID

    code: str

    name: str

    price: Decimal