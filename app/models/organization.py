"""
Organization Model

Represents a tenant/company in the SentriqVision platform.
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    String,
    Boolean,
    Enum,
    Text,
    Integer,
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
    EXPIRED = "EXPIRED"


# ==========================================================
# Organization
# ==========================================================
class Organization(BaseModel):
    """
    Organization / Company
    """

    __tablename__ = "organizations"

    # ------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------

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

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    logo_url: Mapped[str | None] = mapped_column(
        String(500),
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
    )

    # ------------------------------------------------------
    # Contact
    # ------------------------------------------------------

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
    )

    alternate_phone: Mapped[str | None] = mapped_column(
        String(20),
    )

    # ------------------------------------------------------
    # Address
    # ------------------------------------------------------

    address: Mapped[str | None] = mapped_column(
        Text,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default="Asia/Kolkata",
    )

    # ------------------------------------------------------
    # Business
    # ------------------------------------------------------

    gst_number: Mapped[str | None] = mapped_column(
        String(30),
    )

    registration_number: Mapped[str | None] = mapped_column(
        String(100),
    )

    industry_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    employee_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ------------------------------------------------------
    # Subscription
    # ------------------------------------------------------

    status: Mapped[OrganizationStatus] = mapped_column(
        Enum(OrganizationStatus),
        default=OrganizationStatus.ACTIVE,
        nullable=False,
    )

    trial_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ------------------------------------------------------
    # Relationships
    # ------------------------------------------------------

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

    services = relationship(
        "OrganizationService",
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

    cameras = relationship(
        "Camera",
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

    # ------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<Organization("
            f"name='{self.name}', "
            f"code='{self.organization_code}')>"
        )