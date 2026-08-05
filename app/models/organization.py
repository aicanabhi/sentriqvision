"""
Organization Model

Represents an Organization in the SentriQVision Platform.
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Enum,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import BaseModel


# ==========================================================
# Organization Status
# ==========================================================

class OrganizationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


# ==========================================================
# Organization Model
# ==========================================================

class Organization(
    BaseModel,
):
    """
    Organization Model
    """

    __tablename__ = "organizations"

    # ======================================================
    # Basic Information
    # ======================================================

    organization_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # ======================================================
    # Status
    # ======================================================

    status: Mapped[OrganizationStatus] = mapped_column(
        Enum(OrganizationStatus),
        default=OrganizationStatus.ACTIVE,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    users = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    teams = relationship(
        "Team",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    roles = relationship(
        "Role",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    cameras = relationship(
        "Camera",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    settings = relationship(
        "OrganizationSetting",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )

    subscription = relationship(
        "OrganizationSubscription",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )

    services = relationship(
        "OrganizationService",
        back_populates="organization",
        cascade="all, delete-orphan",
    )


    parking_zones = relationship(
        "ParkingZone",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    parking_slots = relationship(
        "ParkingSlot",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    alerts = relationship(
        "Alert",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    reports = relationship(
        "Report",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    audits = relationship(
        "Audit",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    events = relationship(
        "Event",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    detections = relationship(
        "Detection",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    notifications = relationship(
        "Notification",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    ai_models = relationship(
        "AIModel",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Organization("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"code='{self.organization_code}')>"
        )