
from typing import Optional
from app.application.repositories.base_repository import BaseRepository


class OrganizationAdminRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "organization_admins")

    async def get_by_email(self, email: str) -> Optional[dict]:
        return await self.get_by_field("email", email)

    async def get_by_organization_id(self, organization_id: str) -> Optional[dict]:
        return await self.get_by_field("organization_id", organization_id)
