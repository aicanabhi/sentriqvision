import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.site import Site

class SiteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            site_id: uuid.UUID,
    ) -> Site | None:
        result = await self.session.execute(select(Site).where(Site.id == site_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Site]:
        result = await self.session.execute(select(Site).order_by(Site.id))
        return list(result.scalars().all())

    async def get_by_organization(
            self,
            organization_id: uuid.UUID,
    ) -> list[Site]:
        result = await self.session.execute(
            select(Site)
            .where(Site.organization_id == organization_id)
            .order_by(Site.name)
        )
        return list (result.scalars().all())

    async def create(
            self,
            organization_id: uuid.UUID,
            name: str,
            timezone: str = "UTC",
            status: str = "ACTIVE",
    ) -> Site:
        site = Site(
            organization_id=organization_id,
            name=name,
            timezone=timezone,
            status=status,
        )

        self.session.add(site)
        await self.session.flush()

        return site

    async def delete(self, site: Site) -> None:
        self.session.delete(site)