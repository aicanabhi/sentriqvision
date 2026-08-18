import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.camera_module import CameraModule
from app.repositories.camera_module import CameraModuleRepository

class CameraModuleService:
    def __init__(self, session: AsyncSession):
        self.repository = CameraModuleRepository(session)

    async def get_by_id(self, camera_module_id: uuid.UUID) -> CameraModule | None:
        return await self.repository.get_by_id(camera_module_id)

    async def get_all(self) -> list[CameraModule]:
        return await self.repository.get_all()

    async def get_by_camera(self, camera_id: uuid.UUID) -> list[CameraModule]:
        return await self.repository.get_by_camera(camera_id)

    async def get_by_module(self, module_id: uuid.UUID) -> list[CameraModule]:
        return await self.repository.get_by_module(module_id)

    async def create(
            self,
            camera_id: CameraModule,
            module_id: uuid.UUID,
            enabled: bool = True
    ) -> CameraModule:

        existing = await self.repository.get_by_camera_and_module(camera_id, module_id)

        if existing is not None:
            raise ValueError(
                "This camera module already exists."
            )

        return await self.repository.create(
            camera_id=camera_id,
            module_id=module_id,
            enabled=enabled,
        )

    async def delete(self, camera_module_id: uuid.UUID) -> None:
        camera_module = await self.repository.get_by_id(camera_module_id)

        if camera_module is None:
            raise ValueError(
                "Camera module mapping not found."
            )

        await self.repository.delete(camera_module)