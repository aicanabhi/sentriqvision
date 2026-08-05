"""
Role Repository

Database operations for Role model.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """
    Repository for Role database operations.
    """


    def __init__(self, db: AsyncSession):
        super().__init__(
            db=db,
            model=Role
        )


    # ======================================================
    # Get Role By Name
    # ======================================================

    async def get_by_name(
        self,
        name: str,
        organization_id: Optional[UUID] = None
    ) -> Optional[Role]:

        query = select(Role).where(
            Role.name == name
        )


        if organization_id:
            query = query.where(
                Role.organization_id == organization_id
            )


        result = await self.db.execute(query)

        return result.scalar_one_or_none()



    # ======================================================
    # Get Roles By Organization
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID
    ) -> List[Role]:

        query = select(Role).where(
            Role.organization_id == organization_id
        )

        result = await self.db.execute(query)

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Check Role Exists
    # ======================================================

    async def exists(
        self,
        name: str,
        organization_id: UUID
    ) -> bool:

        role = await self.get_by_name(
            name=name,
            organization_id=organization_id
        )

        return role is not None



    # ======================================================
    # Get Active Roles
    # ======================================================

    async def get_active_roles(
        self,
        organization_id: UUID
    ) -> List[Role]:

        query = select(Role).where(
            Role.organization_id == organization_id,
            Role.is_active == True
        )


        result = await self.db.execute(query)

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Get Role With Permissions
    # ======================================================

    async def get_with_permissions(
        self,
        role_id: UUID
    ) -> Optional[Role]:

        query = (
            select(Role)
            .where(Role.id == role_id)
        )


        result = await self.db.execute(query)

        return result.scalar_one_or_none()



    # ======================================================
    # Delete Role
    # ======================================================

    async def delete_role(
        self,
        role_id: UUID
    ) -> bool:

        role = await self.get(role_id)

        if not role:
            return False


        await self.delete(role)

        return True