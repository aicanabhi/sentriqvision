"""
Organization Subscription Model

Links organizations with subscription plans.
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import UUID
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
# Subscription Status
# ==========================================================

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    TRIAL = "TRIAL"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"


# ==========================================================
# Payment Status
# ==========================================================

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


# ==========================================================
# Organization Subscription
# ==========================================================

class OrganizationSubscription(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):
    """
    Organization Subscription
    """

    __tablename__ = "organization_subscriptions"

    # ======================================================
    # Foreign Keys
    # ======================================================

    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    plan_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "plans.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Subscription Details
    # ======================================================

    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus),
        default=SubscriptionStatus.TRIAL,
        nullable=False,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    # ======================================================
    # Dates
    # ======================================================

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    trial_end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    # ======================================================
    # Subscription Options
    # ======================================================

    auto_renew: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_trial: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ======================================================
    # Payment Information
    # ======================================================

    transaction_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    payment_reference: Mapped[str | None] = mapped_column(
        String(255),
    )

    payment_provider: Mapped[str | None] = mapped_column(
        String(100),
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="subscription",
    )

    plan = relationship(
        "Plan",
        back_populates="subscriptions",
    )

    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<OrganizationSubscription("
            f"organization='{self.organization_id}', "
            f"plan='{self.plan_id}', "
            f"status='{self.status}')>"
        )