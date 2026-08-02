"""
Parking Schemas

Handles:
- Parking Zones
- Parking Slots
- Parking Availability
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Parking Zone
# ==========================================================


class ParkingZoneBase(BaseSchema):
    """
    Base parking zone schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    description: Optional[str] = None

    camera_id: Optional[UUID] = None

    total_slots: int = Field(
        default=0,
        ge=0,
    )

    is_active: bool = True



# ==========================================================
# Create Zone
# ==========================================================


class ParkingZoneCreate(ParkingZoneBase):
    """
    Create parking zone.
    """

    organization_id: UUID



# ==========================================================
# Update Zone
# ==========================================================


class ParkingZoneUpdate(BaseSchema):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    camera_id: Optional[UUID] = None

    is_active: Optional[bool] = None



# ==========================================================
# Zone Response
# ==========================================================


class ParkingZoneResponse(BaseResponseSchema):

    organization_id: UUID

    name: str

    code: str

    description: Optional[str]

    camera_id: Optional[UUID]

    total_slots: int

    available_slots: int = 0

    occupied_slots: int = 0

    is_active: bool



# ==========================================================
# Zone List
# ==========================================================


class ParkingZoneListResponse(BaseSchema):

    zones: list[ParkingZoneResponse]

    total: int

    page: int

    page_size: int



# ==========================================================
# Parking Slot
# ==========================================================


class ParkingSlotBase(BaseSchema):

    slot_number: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    zone_id: UUID

    slot_type: str = Field(
        default="CAR",
        max_length=30,
    )

    floor: Optional[str] = None

    is_active: bool = True



# ==========================================================
# Create Slot
# ==========================================================


class ParkingSlotCreate(ParkingSlotBase):
    pass



# ==========================================================
# Update Slot
# ==========================================================


class ParkingSlotUpdate(BaseSchema):

    slot_number: Optional[str] = None

    slot_type: Optional[str] = None

    floor: Optional[str] = None

    is_active: Optional[bool] = None



# ==========================================================
# Slot Response
# ==========================================================


class ParkingSlotResponse(BaseResponseSchema):

    zone_id: UUID

    slot_number: str

    slot_type: str

    floor: Optional[str]

    status: str

    vehicle_number: Optional[str] = None

    is_active: bool



# ==========================================================
# Slot Status Update
# ==========================================================


class ParkingSlotStatusUpdate(BaseSchema):

    status: str = Field(
        ...,
        description="AVAILABLE / OCCUPIED / RESERVED"
    )

    vehicle_number: Optional[str] = None



# ==========================================================
# Parking Filter
# ==========================================================


class ParkingFilter(BaseSchema):

    organization_id: Optional[UUID] = None

    zone_id: Optional[UUID] = None

    status: Optional[str] = None

    slot_type: Optional[str] = None

    search: Optional[str] = None

    page: int = 1

    page_size: int = 20



# ==========================================================
# Parking Statistics
# ==========================================================


class ParkingStatistics(BaseSchema):

    total_slots: int = 0

    occupied_slots: int = 0

    available_slots: int = 0

    reserved_slots: int = 0

    occupancy_percentage: float = 0.0



# ==========================================================
# Delete Response
# ==========================================================


class ParkingDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "Parking record deleted successfully."