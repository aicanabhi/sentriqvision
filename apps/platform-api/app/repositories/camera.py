import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.camera import Camera

class CameraRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            camera_id: uuid.UUID,
    ) -> Camera | None:
        result = await self.session.execute(
            select(Camera).where(Camera.id == camera_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Camera]:
        result = await self.session.execute(
            select(Camera).order_by(Camera.name)
        )
        return list(result.scalars().all())

    async def get_by_site(self, site_id: uuid.UUID) -> list[Camera]:
        result = await self.session.execute(
            select(Camera).where(Camera.site_id == site_id).order_by(Camera.name)
        )
        return list(result.scalars().all())

    async def get_by_zone(self, zone_id: uuid.UUID) -> list[Camera]:
        result = await self.session.execute(
            select(Camera).where(Camera.zone == zone_id).order_by(Camera.name)
        )
        return list(result.scalars().all())

    async def create (
            self,
            site_id: uuid.UUID,
            zone_id: uuid.UUID,
            camera_code: str,
            name: str,
            rtsp_url: str,
            resolution: str = "1080p",
            fps: int = 25,
            status: str = "OFFLINE",
    ) -> Camera:
        camera = Camera(
            site_id = site_id,
            zone_id = zone_id,
            camera_code = camera_code,
            name = name,
            rtsp_url = rtsp_url,
            resolution = resolution,
            fps = fps,
            status = status,
        )
        self.session.add(camera)
        await self.session.flush()
        return camera

    async def delete(self, camera: Camera) -> None:
        await self.session.delete(camera)