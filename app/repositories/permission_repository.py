"""
Permission Repository

Handles all database operations related to permissions.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.repositories.base_repository import BaseRepository


class PermissionRepository(
    BaseRepository[Permission]
):

    def __init__(
        self,
        db: AsyncSession
    ):
        super().__init__(
            db,
            Permission
        )


    # ======================================================
    # Get Permission By Code
    # ======================================================

    async def get_by_code(
        self,
        code: str
    ) -> Optional[Permission]:

        result = await self.db.execute(
            select(Permission)
            .where(
                Permission.code == code
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # Get Permission By Name
    # ======================================================

    async def get_by_name(
        self,
        name: str
    ) -> Optional[Permission]:

        result = await self.db.execute(
            select(Permission)
            .where(
                Permission.name == name
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # List Permissions
    # ======================================================

    async def get_all_permissions(
        self,
        search: Optional[str] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Permission]:


        query = select(Permission)


        if search:

            query = query.where(
                or_(
                    Permission.name.ilike(
                        f"%{search}%"
                    ),

                    Permission.code.ilike(
                        f"%{search}%"
                    )
                )
            )


        if module:

            query = query.where(
                Permission.module == module
            )


        if action:

            query = query.where(
                Permission.action == action
            )


        if is_active is not None:

            query = query.where(
                Permission.is_active == is_active
            )


        result = await self.db.execute(
            query
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Get Permissions By IDs
    # ======================================================

    async def get_by_ids(
        self,
        permission_ids: list[UUID]
    ) -> List[Permission]:


        result = await self.db.execute(
            select(Permission)
            .where(
                Permission.id.in_(
                    permission_ids
                )
            )
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Activate Permission
    # ======================================================

    async def activate(
        self,
        permission_id: UUID
    ):


        await self.db.execute(
            update(Permission)
            .where(
                Permission.id == permission_id
            )
            .values(
                is_active=True
            )
        )

        await self.db.commit()



    # ======================================================
    # Deactivate Permission
    # ======================================================

    async def deactivate(
        self,
        permission_id: UUID
    ):


        await self.db.execute(
            update(Permission)
            .where(
                Permission.id == permission_id
            )
            .values(
                is_active=False
            )
        )

        await self.db.commit()



    # ======================================================
    # Delete Permission
    # ======================================================

    async def delete_permission(
        self,
        permission_id: UUID
    ):

        await self.db.execute(
            delete(Permission)
            .where(
                Permission.id == permission_id
            )
        )

        await self.db.commit()