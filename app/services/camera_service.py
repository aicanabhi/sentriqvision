"""
Camera Service Layer

Business logic for camera management.
"""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera import Camera


class CameraService:

    def __init__(self, db: AsyncSession):
        self.db = db


    # ======================================================
    # Create Camera
    # ======================================================

    async def create_camera(self, camera_data):

        camera = Camera(
            organization_id=str(camera_data.organization_id),
            camera_group_id=(
                str(camera_data.camera_group_id)
                if camera_data.camera_group_id
                else None
            ),

            name=camera_data.name,
            description=camera_data.description,
            location=camera_data.location,

            ip_address=camera_data.ip_address,
            port=camera_data.port,

            manufacturer=camera_data.manufacturer,
            model_name=camera_data.model,
            serial_number=camera_data.serial_number,

            rtsp_url=camera_data.rtsp_url,
            username=camera_data.username,
            password=camera_data.password,

            resolution=camera_data.resolution,
            fps=camera_data.fps,
            codec=camera_data.codec,

            ai_enabled=camera_data.ai_enabled,
        )


        self.db.add(camera)

        await self.db.commit()

        await self.db.refresh(camera)

        return camera



    # ======================================================
    # Get Cameras
    # ======================================================

    async def get_cameras(
        self,
        organization_id: UUID | None = None,
    ):

        query = select(Camera)


        if organization_id:
            query = query.where(
                Camera.organization_id == str(organization_id)
            )


        result = await self.db.execute(query)


        return result.scalars().all()



    # ======================================================
    # Get Single Camera
    # ======================================================

    async def get_camera(
        self,
        camera_id: UUID
    ):

        result = await self.db.execute(
            select(Camera).where(
                Camera.id == str(camera_id)
            )
        )


        return result.scalar_one_or_none()



    # ======================================================
    # Update Camera
    # ======================================================

    async def update_camera(
        self,
        camera_id: UUID,
        camera_data,
    ):

        camera = await self.get_camera(camera_id)


        if not camera:
            return None


        data = camera_data.model_dump(
            exclude_unset=True
        )


        for key,value in data.items():

            if hasattr(camera,key):
                setattr(
                    camera,
                    key,
                    value
                )


        await self.db.commit()

        await self.db.refresh(camera)


        return camera



    # ======================================================
    # Delete Camera
    # ======================================================

    async def delete_camera(
        self,
        camera_id: UUID
    ):


        camera = await self.get_camera(camera_id)


        if not camera:
            raise HTTPException(
                status_code=404,
                detail="Camera not found"
            )


        await self.db.delete(camera)

        await self.db.commit()


        return {
            "success":True,
            "message":"Camera deleted successfully"
        }



    # ======================================================
    # Stream
    # ======================================================

    async def start_stream(
        self,
        camera_id: UUID
    ):

        return {
            "success":True,
            "message":"Camera stream started"
        }



    async def stop_stream(
        self,
        camera_id: UUID
    ):

        return {
            "success":True,
            "message":"Camera stream stopped"
        }