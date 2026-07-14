
from typing import Optional
from app.application.repositories.base_repository import BaseRepository


class SuperAdminRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "super_admin")

    async def get_by_email(self, email: str) -> Optional[dict]:
        return await self.get_by_field("email", email)
