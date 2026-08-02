"""
Common API Schemas
"""

from __future__ import annotations

from math import ceil
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ==========================================================
# API Response
# ==========================================================

class APIResponse(BaseModel, Generic[T]):
    """
    Standard API Response
    """

    model_config = ConfigDict(from_attributes=True)

    success: bool = True

    message: str = "Success"

    data: Optional[T] = None


# ==========================================================
# Error Response
# ==========================================================

class ErrorResponse(BaseModel):

    success: bool = False

    message: str

    error: Optional[Any] = None


# ==========================================================
# Pagination Request
# ==========================================================

class PaginationParams(BaseModel):

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )


# ==========================================================
# Pagination Meta
# ==========================================================

class PaginationMeta(BaseModel):

    page: int

    page_size: int

    total_items: int

    total_pages: int

    has_next: bool

    has_previous: bool

    @classmethod
    def create(
        cls,
        page: int,
        page_size: int,
        total_items: int,
    ):

        total_pages = ceil(total_items / page_size) if total_items else 1

        return cls(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


# ==========================================================
# Paginated Response
# ==========================================================

class PaginatedResponse(BaseModel, Generic[T]):

    success: bool = True

    message: str = "Success"

    items: List[T]

    pagination: PaginationMeta


# ==========================================================
# Search Request
# ==========================================================

class SearchParams(PaginationParams):

    search: Optional[str] = None

    sort_by: Optional[str] = "created_at"

    sort_order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
    )


# ==========================================================
# Generic ID Response
# ==========================================================

class IDResponse(BaseModel):

    id: str


# ==========================================================
# Health Check
# ==========================================================

class HealthResponse(BaseModel):

    status: str = "healthy"

    version: str

    environment: str