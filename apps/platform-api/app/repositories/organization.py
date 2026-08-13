import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization

class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            organization_id: uuid.UUID,
    ) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Organization]:
        result = await self.session.execute(
            select(Organization).order_by(Organization.name)
        )
        return list(result.scalars().all())

    async def create(self, name: str, status: str = "ACTIVE") -> Organization:
        organization = Organization(
            name=name,
            status=status,
        )
        self.session.add(organization)
        await self.session.flush()
        return organization

    async def delete(self, organization: Organization,) -> None:
        await self.session.delete(organization)