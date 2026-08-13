import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.site import Site
from app.repositories.site import SiteRepository

class SiteService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = SiteRepository(session)

    async def get_by_id(
            self,
            site_id: uuid.UUID,
    ) -> Site | None:
        return await self.repository.get_by_id(site_id)

    async def get_all(self) -> list[Site]:
        return await self.repository.get_all()

    async def get_by_organization(
            self,
            organization_id: uuid.UUID,
    ) -> list[Site]:
        return await self.repository.get_by_organization(organization_id)

    async def create(
            self,
            organization_id: uuid.UUID,
            name: str,
            timezone: str = "UTC",
            status: str = "ACTIVE",
    ) -> Site:
        name = name.strip()

        if not name:
            raise ValueError("Site name is required")

        return await self.repository.create(
            organization_id=organization_id,
            name=name,
            timezone=timezone,
            status=status,
        )

    async def delete(self, site_id: uuid.UUID) -> None:
        site = await self.repository.get_by_id(site_id)

        if sita is None:
            raise ValueError("Site not found")

        await self.repository.delete(site)