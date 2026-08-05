"""
Role Service
"""
from fastapi import APIRouter

router = APIRouter()
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

        role = Role(**role_data.model_dump())

        self.db.add(role)

        await self.db.commit()
        await self.db.refresh(role)

        return role

    # ==========================================================
    # List Roles
    # ==========================================================

    async def list_roles(
        self,
        page: int = 1,
        per_page: int = 20,
    ):

        offset = (page - 1) * per_page

        result = await self.db.execute(
            select(Role)
            .offset(offset)
            .limit(per_page)
        )

        return result.scalars().all()

    # ==========================================================
    # Get Role
    # ==========================================================

    async def get_role(self, role_id):

        result = await self.db.execute(
            select(Role)
            .where(Role.id == str(role_id))
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

        if role is None:
            return None

        data = role_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for key, value in data.items():
            setattr(role, key, value)

        await self.db.commit()
        await self.db.refresh(role)

        return role

    # ==========================================================
    # Delete Role
    # ==========================================================

    async def delete_role(self, role_id):

        role = await self.get_role(role_id)

        if role is None:
            return False

        await self.db.delete(role)
        await self.db.commit()

        return True

    # ==========================================================
    # Assign Permissions
    # ==========================================================

    async def assign_permissions(
        self,
        role_id,
        permission_ids,
    ):

        role = await self.get_role(role_id)

        if role is None:
            return None

        # TODO:
        # Permission model ready hone ke baad
        # yahan permission assign karenge.

        return {
            "success": True,
            "message": "Permissions assigned successfully."
        }

    # ==========================================================
    # Remove Permission
    # ==========================================================

    async def remove_permission(
        self,
        role_id,
        permission_id,
    ):

        role = await self.get_role(role_id)

        if role is None:
            return None

        # TODO:
        # Permission remove logic

        return {
            "success": True,
            "message": "Permission removed successfully."
        }

    # ==========================================================
    # Get Role Permissions
    # ==========================================================

    async def get_role_permissions(
        self,
        role_id,
    ):

        role = await self.get_role(role_id)

        if role is None:
            return None

        # TODO:
        # Actual permissions baad me

        return []