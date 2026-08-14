import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.camera import Camera
from app.repositories.camera import CameraRepository

class CameraService:
    def __init__(self, session: AsyncSession):
        self.repository = CameraRepository(session)

    async def get_by_id(self, camera_id: uuid.UUID) -> Camera | None:
        return await self.repository.get_by_id(camera_id)

    async def get_all(self) -> list[Camera]:
        return await self.repository.get_all()

    async def get_by_site(self, site_id: uuid.UUID) -> list[Camera]:
        return await self.repository.get_by_site(site_id)

    async def get_by_zone(self, zone_id: uuid.UUID) -> list[Camera]:
        return await self.repository.get_by_zone(zone_id)

    async def create(
            self,
            site_id: uuid.UUID,
            zone_id: uuid.UUID,
            camera_code: str,
            name: str,
            rtsp_url: str,
            resolution: str = "1080p",
            fps: int = 25,
            status: str = "OFFLINE"
    ) -> Camera:
        camera = Camera(
            camera_code = camera_code.strip(),
            name = name.strip(),
            rtsp_url = rtsp_url.strip(),
        )

        if not camera_code:
            raise ValueError("Camera Code cannot be empty")

        if not name:
            raise ValueError("Camera Name cannot be empty")

        if not rtsp_url:
            raise ValueError("RTSP URL cannot be empty")

        if fps<=0:
            raise ValueError("FPS must be greater than 0")

        return await self.repository.create(
            site_id = site_id,
            zone_id = zone_id,
            camera_code = camera_code,
            name = name,
            rtsp_url = rtsp_url,
            resolution = resolution,
            fps = fps,
            status = status
        )

    async def delete(self, camera_id: uuid.UUID) -> None:
        camera = await self.repository.get_by_id(camera_id)

        if camera is None:
            raise ValueError("Camera does not exist")

        await self.repository.delete(camera)