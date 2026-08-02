"""
Base Pydantic Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with ORM support."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
        protected_namespaces=(),
    )


class TimestampSchema(BaseSchema):
    """Created / Updated timestamps."""

    created_at: datetime
    updated_at: datetime


class UUIDSchema(BaseSchema):
    """UUID primary key."""

    id: UUID


class ActiveSchema(BaseSchema):
    """Entity active status."""

    is_active: bool = True


class SoftDeleteSchema(BaseSchema):
    """Soft delete fields."""

    is_deleted: bool = False
    deleted_at: Optional[datetime] = None


class AuditSchema(BaseSchema):
    """Audit information."""

    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None


class BaseResponseSchema(
    UUIDSchema,
    TimestampSchema,
    ActiveSchema,
):
    """
    Standard response model
    for almost every entity.
    """

    pass