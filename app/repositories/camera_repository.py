"""
Camera Repository

Database operations for cameras.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera import Camera
from app.models.camera_health import CameraHealth
from app.models.camera_stream import CameraStream

from app.repositories.base_repository import BaseRepository


class CameraRepository(BaseRepository[Camera]):
    """
    Camera database repository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(
            db=db,
            model=Camera
        )


    # ======================================================
    # Get by organization
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[Camera]:

        query = (
            select(Camera)
            .where(
                Camera.organization_id == organization_id
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Get active cameras
    # ======================================================

    async def get_active_cameras(
        self,
        organization_id: UUID
    ) -> List[Camera]:

        query = (
            select(Camera)
            .where(
                Camera.organization_id == organization_id,
                Camera.is_active == True
            )
        )

        result = await self.db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Find camera by name
    # ======================================================

    async def get_by_name(
        self,
        name: str,
        organization_id: UUID
    ) -> Optional[Camera]:

        query = (
            select(Camera)
            .where(
                Camera.name == name,
                Camera.organization_id == organization_id
            )
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()



    # ======================================================
    # Update camera status
    # ======================================================

    async def update_status(
        self,
        camera_id: UUID,
        status: str
    ):

        query = (
            update(Camera)
            .where(
                Camera.id == camera_id
            )
            .values(
                status=status
            )
        )

        await self.db.execute(query)

        await self.db.commit()



    # ======================================================
    # Count cameras
    # ======================================================

    async def count_by_organization(
        self,
        organization_id: UUID
    ) -> int:

        query = (
            select(
                func.count(Camera.id)
            )
            .where(
                Camera.organization_id == organization_id
            )
        )

        result = await self.db.execute(query)

        return result.scalar()



    # ======================================================
    # Camera Health
    # ======================================================

    async def get_health(
        self,
        camera_id: UUID
    ) -> Optional[CameraHealth]:

        query = (
            select(CameraHealth)
            .where(
                CameraHealth.camera_id == camera_id
            )
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()



    async def update_health(
        self,
        camera_id: UUID,
        health_data: dict
    ):

        query = (
            update(CameraHealth)
            .where(
                CameraHealth.camera_id == camera_id
            )
            .values(
                **health_data
            )
        )

        await self.db.execute(query)

        await self.db.commit()



    # ======================================================
    # Camera Stream
    # ======================================================

    async def get_stream(
        self,
        camera_id: UUID
    ) -> Optional[CameraStream]:

        query = (
            select(CameraStream)
            .where(
                CameraStream.camera_id == camera_id
            )
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()



    async def update_stream(
        self,
        camera_id: UUID,
        stream_data: dict
    ):

        query = (
            update(CameraStream)
            .where(
                CameraStream.camera_id == camera_id
            )
            .values(
                **stream_data
            )
        )

        await self.db.execute(query)

        await self.db.commit()



    # ======================================================
    # Delete Camera
    # ======================================================

    async def delete_camera(
        self,
        camera_id: UUID
    ):

        query = (
            delete(Camera)
            .where(
                Camera.id == camera_id
            )
        )

        await self.db.execute(query)

        await self.db.commit()