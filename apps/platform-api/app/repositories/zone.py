import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.zone import Zone

class ZoneRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            zone_id: uuid.UUID,
    ) -> Zone | None:
        result = await self.session.execute(select(Zone).where(Zone.id == zone_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Zone]:
        result = await self.session.execute(select(Zone).order_by(Zone.id))
        return list(result.scalars().all())

    async def get_by_site(self, site_id: uuid.UUID,) -> list[Zone]:
        result = await self.session.execute(select(Zone).where(Zone.site_id == site_id).order_by(Zone.name))
        return list(result.scalars().all())

    async def create(
            self,
            site_id: uuid.UUID,
            name: str,
            zone_type: str,
            status: str = "ACTIVE",
    ) -> Zone:
        zone = Zone(
            site_id = site_id,
            name = name,
            zone_type = zone_type,
            status = status,
        )
        self.session.add(zone)
        await self.session.flush()

        return zone

    async def delete(self, zone: Zone) -> None:
        await self.session.delete(zone)