"""
SQLAlchemy Base Models

Contains:
- Declarative Base
- Common Model Mixins
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ==========================================================
# Main SQLAlchemy Base
# ==========================================================

class Base(DeclarativeBase):
    pass


# ==========================================================
# UUID Mixin
# ==========================================================

class UUIDMixin:
    """
    Adds UUID primary key
    """

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
        index=True,
    )


# ==========================================================
# Timestamp Mixin
# ==========================================================

class TimestampMixin:
    """
    Adds created_at and updated_at timestamps
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# ==========================================================
# Active Status Mixin
# ==========================================================

class ActiveMixin:
    """
    Adds active/inactive status
    """

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )


# ==========================================================
# Soft Delete Mixin
# ==========================================================

class SoftDeleteMixin:
    """
    Adds soft delete support
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


# ==========================================================
# Audit Mixin
# ==========================================================

class AuditMixin:
    """
    Stores audit information
    """

    created_by: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    updated_by: Mapped[str | None] = mapped_column(
        nullable=True,
    )


# ==========================================================
# Common Base Model (Optional)
# ==========================================================

class BaseModel(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Common fields for all models
    """

    __abstract__ = True