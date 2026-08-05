"""
Camera Group Service
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_group import CameraGroup


class CameraGroupService:


    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db



    async def create(
        self,
        data
    ):

        group = CameraGroup(
            **data.model_dump()
        )

        self.db.add(group)

        await self.db.commit()

        await self.db.refresh(group)

        return group



    async def get_all(self):

        result = await self.db.execute(
            select(CameraGroup)
        )

        return result.scalars().all()



    async def get_by_id(
        self,
        group_id: UUID
    ):

        result = await self.db.execute(
            select(CameraGroup)
            .where(
                CameraGroup.id == str(group_id)
            )
        )

        return result.scalar_one_or_none()



    async def update(
        self,
        group_id,
        data
    ):

        group = await self.get_by_id(
            group_id
        )

        if not group:
            return None


        update_data = data.model_dump(
            exclude_unset=True
        )


        for key,value in update_data.items():

            setattr(
                group,
                key,
                value
            )


        await self.db.commit()

        await self.db.refresh(group)

        return group



    async def delete(
        self,
        group_id
    ):

        group = await self.get_by_id(
            group_id
        )

        if not group:
            return False


        await self.db.delete(group)

        await self.db.commit()


        return True