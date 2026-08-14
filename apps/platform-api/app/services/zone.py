import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.zone import Zone
from app.repositories.zone import ZoneRepository

class ZoneService:
    def __init__(self, session: AsyncSession):
        self.repository = ZoneRepository(session)

    async def get_by_id(
            self,
            zone_id: uuid.UUID,
    ) -> Zone | None:
        return await self.repository.get_by_id(zone_id)

    async def get_all(self) -> list[Zone]:
        return await self.repository.get_all()

    async def get_by_site(
            self,
            site_id: uuid.UUID,
    ) -> list[Zone]:
        return await self.repository.get_by_site(site_id)

    async def create(
            self,
            site_id: uuid.UUID,
            name: str,
            zone_type: str,
            status: str = "ACTIVE",
    ) -> Zone:
        name = name.strip()
        zone_type = zone_type.strip()

        if not name:
            raise ValueError("Zone name cannot be empty")

        if not zone_type:
            raise ValueError("Zone type cannot be empty")

        return await self.repository.create(
            site_id=site_id,
            name=name,
            zone_type=zone_type,
            status=status,
        )

    async def delete(
            self,
            zone_id: uuid.UUID,
    ) -> None:
        zone = await self.repository.get_by_id(zone_id)

        if zone is None:
            raise ValueError("Zone not found")

        await self.repository.delete(zone)