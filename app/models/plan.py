"""
Subscription Plan Model

Defines available subscription plans for organizations.
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Enum,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    ActiveMixin,
    Base,
    TimestampMixin,
    UUIDMixin,
)


# ==========================================================
# Plan Billing Cycle
# ==========================================================

class BillingCycle(str, enum.Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    LIFETIME = "LIFETIME"


# ==========================================================
# Plan Model
# ==========================================================

class Plan(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):
    """
    Subscription Plan
    """

    __tablename__ = "plans"

    # ------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    # ------------------------------------------------------
    # Pricing
    # ------------------------------------------------------

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    billing_cycle: Mapped[BillingCycle] = mapped_column(
        Enum(BillingCycle),
        default=BillingCycle.MONTHLY,
        nullable=False,
    )

    trial_days: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ------------------------------------------------------
    # Limits
    # ------------------------------------------------------

    max_users: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )

    max_teams: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )

    max_cameras: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )

    max_storage_gb: Mapped[int] = mapped_column(
        Integer,
        default=100,
    )

    # ------------------------------------------------------
    # AI Features
    # ------------------------------------------------------

    ai_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    gpu_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    api_access: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    analytics_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    reports_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    priority_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ------------------------------------------------------
    # Relationships
    # ------------------------------------------------------

    subscriptions = relationship(
        "OrganizationSubscription",
        back_populates="plan",
        cascade="all, delete-orphan",
    )

    # ------------------------------------------------------

    def __repr__(self) -> str:
        return f"<Plan(name='{self.name}', price={self.price})>"