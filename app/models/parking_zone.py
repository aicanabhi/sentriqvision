"""
Enterprise Parking Zone Model
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    ActiveMixin,
    AuditMixin,
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)


# ==========================================================
# Zone Type
# ==========================================================

class ParkingZoneType(str, enum.Enum):
    VISITOR = "VISITOR"
    STAFF = "STAFF"
    VIP = "VIP"
    RESERVED = "RESERVED"
    EV = "EV"
    TRUCK = "TRUCK"
    BIKE = "BIKE"
    MIXED = "MIXED"


# ==========================================================
# Parking Zone
# ==========================================================

class ParkingZone(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "parking_zones"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "name",
            name="uq_parking_zone_name_org",
        ),
    )

    # ======================================================
    # Organization
    # ======================================================

    organization_id: Mapped[str] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Camera Group
    # ======================================================

    camera_group_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "camera_groups.id",
            ondelete="SET NULL",
        )
    )

    # ======================================================
    # Basic Information
    # ======================================================

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str | None] = mapped_column(
        String(50),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    zone_type: Mapped[ParkingZoneType] = mapped_column(
        Enum(ParkingZoneType),
        default=ParkingZoneType.MIXED,
    )

    # ======================================================
    # Capacity
    # ======================================================

    total_slots: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    occupied_slots: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    available_slots: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ======================================================
    # Polygon
    # ======================================================

    polygon: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # Example
    # {
    #   "points":[
    #      [120,200],
    #      [350,210],
    #      [360,500],
    #      [100,490]
    #   ]
    # }

    # ======================================================
    # AI Configuration
    # ======================================================

    ai_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    wrong_parking_detection: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    occupancy_detection: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    entry_exit_detection: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="parking_zones",
    )

    camera_group = relationship(
        "CameraGroup",
    )

    parking_slots = relationship(
        "ParkingSlot",
        back_populates="parking_zone",
        cascade="all, delete-orphan",
    )

    # ======================================================

    @property
    def occupancy_percentage(self) -> float:
        if self.total_slots == 0:
            return 0.0

        return round(
            (self.occupied_slots / self.total_slots) * 100,
            2,
        )

    def __repr__(self) -> str:
        return (
            f"<ParkingZone("
            f"name='{self.name}', "
            f"slots={self.total_slots})>"
        )