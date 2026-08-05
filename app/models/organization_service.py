"""
Organization Service Model

Mapping between Organizations and Services.
"""

from __future__ import annotations

from sqlalchemy import (
    ForeignKey,
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


class OrganizationService(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):
    """
    Organization-Service Mapping
    """

    __tablename__ = "organization_services"

    # =====================================================
    # Foreign Keys
    # =====================================================

    organization_id: Mapped[str] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    service_id: Mapped[str] = mapped_column(
        ForeignKey(
            "services.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    organization = relationship(
        "Organization",
        back_populates="services",
    )

    service = relationship(
        "Service",
        back_populates="organizations",
    )

    configuration = relationship(
        "ServiceConfiguration",
        back_populates="organization_service",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # =====================================================

    def __repr__(self) -> str:
        return (
            f"<OrganizationService("
            f"organization_id={self.organization_id}, "
            f"service_id={self.service_id})>"
        )