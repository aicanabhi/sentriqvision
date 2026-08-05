"""
Enterprise Parking Slot Model
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
    Float,
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
# Parking Slot Status
# ==========================================================

class ParkingSlotStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    BLOCKED = "BLOCKED"
    MAINTENANCE = "MAINTENANCE"


# ==========================================================
# Vehicle Type
# ==========================================================

class ParkingVehicleType(str, enum.Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"
    BUS = "BUS"
    EV = "EV"
    ANY = "ANY"


# ==========================================================
# Parking Slot
# ==========================================================

class ParkingSlot(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "parking_slots"

    __table_args__ = (
        UniqueConstraint(
            "parking_zone_id",
            "slot_number",
            name="uq_slot_number_per_zone",
        ),
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization_id: Mapped[str] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    parking_zone_id: Mapped[str] = mapped_column(
        ForeignKey(
            "parking_zones.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    camera_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "cameras.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ======================================================
    # Basic Info
    # ======================================================

    slot_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    floor: Mapped[str | None] = mapped_column(
        String(30),
    )

    # ======================================================
    # Slot Configuration
    # ======================================================

    vehicle_type: Mapped[ParkingVehicleType] = mapped_column(
        Enum(ParkingVehicleType),
        default=ParkingVehicleType.ANY,
    )

    status: Mapped[ParkingSlotStatus] = mapped_column(
        Enum(ParkingSlotStatus),
        default=ParkingSlotStatus.AVAILABLE,
    )

    is_reserved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_ev_charging: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_disabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Polygon Coordinates
    # ======================================================

    polygon: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # Example:
    # {
    #   "points":[
    #       [100,200],
    #       [250,200],
    #       [250,320],
    #       [100,320]
    #   ]
    # }

    # ======================================================
    # AI Detection
    # ======================================================

    ai_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    confidence_threshold: Mapped[float] = mapped_column(
        Float,
        default=0.60,
    )

    current_confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    # ======================================================
    # Vehicle Details
    # ======================================================

    current_vehicle_number: Mapped[str | None] = mapped_column(
        String(30),
    )

    current_vehicle_type: Mapped[str | None] = mapped_column(
        String(50),
    )

    occupied_since: Mapped[str | None] = mapped_column(
        String(50),
    )

    # ======================================================
    # Statistics
    # ======================================================

    total_occupancy_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_violation_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ======================================================
    # Extra Configuration
    # ======================================================

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="parking_slots",
    )

    parking_zone = relationship(
        "ParkingZone",
        back_populates="parking_slots",
    )

    camera = relationship(
        "Camera",
    )

    # ======================================================

    @property
    def is_available(self) -> bool:
        return self.status == ParkingSlotStatus.AVAILABLE

    @property
    def is_occupied(self) -> bool:
        return self.status == ParkingSlotStatus.OCCUPIED

    # ======================================================

    def __repr__(self):
        return (
            f"<ParkingSlot("
            f"{self.slot_number}, "
            f"{self.status.value})>"
        )