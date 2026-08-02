"""
Parking Repository
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parking_zone import ParkingZone
from app.models.parking_slot import ParkingSlot


class ParkingRepository:
    """
    Repository for Parking Zones and Parking Slots.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # Parking Zones
    # =====================================================

    async def create_zone(self, zone: ParkingZone) -> ParkingZone:
        self.db.add(zone)
        await self.db.commit()
        await self.db.refresh(zone)
        return zone

    async def get_zone_by_id(
        self,
        zone_id: UUID,
    ) -> Optional[ParkingZone]:

        result = await self.db.execute(
            select(ParkingZone).where(
                ParkingZone.id == zone_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all_zones(self) -> list[ParkingZone]:

        result = await self.db.execute(
            select(ParkingZone)
        )

        return result.scalars().all()

    async def update_zone(
        self,
        zone: ParkingZone,
    ) -> ParkingZone:

        await self.db.commit()
        await self.db.refresh(zone)

        return zone

    async def delete_zone(
        self,
        zone: ParkingZone,
    ) -> None:

        await self.db.delete(zone)
        await self.db.commit()

    # =====================================================
    # Parking Slots
    # =====================================================

    async def create_slot(
        self,
        slot: ParkingSlot,
    ) -> ParkingSlot:

        self.db.add(slot)

        await self.db.commit()
        await self.db.refresh(slot)

        return slot

    async def get_slot_by_id(
        self,
        slot_id: UUID,
    ) -> Optional[ParkingSlot]:

        result = await self.db.execute(
            select(ParkingSlot).where(
                ParkingSlot.id == slot_id
            )
        )

        return result.scalar_one_or_none()

    async def get_slots_by_zone(
        self,
        zone_id: UUID,
    ) -> list[ParkingSlot]:

        result = await self.db.execute(
            select(ParkingSlot).where(
                ParkingSlot.zone_id == zone_id
            )
        )

        return result.scalars().all()

    async def get_available_slots(
        self,
        zone_id: UUID,
    ) -> list[ParkingSlot]:

        result = await self.db.execute(
            select(ParkingSlot).where(
                ParkingSlot.zone_id == zone_id,
                ParkingSlot.is_occupied.is_(False),
            )
        )

        return result.scalars().all()

    async def update_slot(
        self,
        slot: ParkingSlot,
    ) -> ParkingSlot:

        await self.db.commit()
        await self.db.refresh(slot)

        return slot

    async def delete_slot(
        self,
        slot: ParkingSlot,
    ) -> None:

        await self.db.delete(slot)
        await self.db.commit()