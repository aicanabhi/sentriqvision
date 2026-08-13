import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
from app.repositories.organization import OrganizationRepository

class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.repository = OrganizationRepository(session)

    async def get_by_id(self, organization_id: uuid.UUID) -> Organization | None:
        return await self.repository.get_by_id(organization_id)

    async def get_all(self) -> list[Organization]:
        return await self.repository.get_all()

    async def create(
            self,
            name: str,
            status: str = "ACTIVE",
    ) -> Organization:
        name = name.strip()

        if not name:
            raise ValueError("Organization name cannot be empty")

        return await self.repository.create(
            name = name,
            status = status,
        )

    async def delete(
            self,
            organization_id: uuid.UUID,
    ) -> None:
        organization = await self.repository.get_by_id(organization_id)
        if organization is None:
            raise ValueError("Organization not found")
        await self.repository.delete(organization)