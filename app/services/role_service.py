"""
Role Service
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role


class RoleService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================================================
    # Create Role
    # ==========================================================

    async def create_role(self, role_data):
        data = role_data.model_dump()

        # UUID ko string me convert karo
        if data.get("organization_id"):
            data["organization_id"] = str(data["organization_id"])
            role = Role(**data)
            self.db.add(role)
            await self.db.commit()
            await self.db.refresh(role)
            return role

    # ==========================================================
    # List Roles
    # ==========================================================

    async def list_roles(self):

        result = await self.db.execute(
            select(Role)
        )

        return result.scalars().all()

    # ==========================================================
    # Get Role
    # ==========================================================

    async def get_role(self, role_id):

        result = await self.db.execute(
            select(Role).where(Role.id == str(role_id))
        )

        return result.scalar_one_or_none()

    # ==========================================================
    # Update Role
    # ==========================================================

    async def update_role(
        self,
        role_id,
        role_data,
    ):

        role = await self.get_role(role_id)

        if not role:
            return None

        data = role_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for key, value in data.items():


            if key == "organization_id" and value:
                value = str(value)
            setattr(role, key, value)

        await self.db.commit()
        await self.db.refresh(role)

        return role

    # ==========================================================
    # Delete Role
    # ==========================================================

    async def delete_role(self, role_id):

        role = await self.get_role(role_id)

        if not role:
            return False

        await self.db.delete(role)
        await self.db.commit()

        return True