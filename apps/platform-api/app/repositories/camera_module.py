import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.camera_module import CameraModule

class CameraModuleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, camera_module_id: uuid.UUID) -> CameraModule | None:
        result = await self.session.execute(select(CameraModule).where(CameraModule.id == camera_module_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[CameraModule]:
        result = await self.session.execute(select(CameraModule).order_by(CameraModule.created_at))
        return list(result.scalars().all())

    async def get_by_camera(self, camera_id: uuid.UUID) -> list[CameraModule]:
        result = await self.session.execute(select(CameraModule).where(CameraModule.camera_id == camera_id).order_by(CameraModule.created_at))
        return list(result.scalars().all())

    async def get_by_module(self, module_id: uuid.UUID) -> list[CameraModule]:
        result = await self.session.execute(select(CameraModule).where(CameraModule.module_id == module_id).order_by(CameraModule.created_at))
        return list(result.scalars().all())

    async def get_by_camera_and_module(self, camera_id: uuid.UUID, module_id: uuid.UUID) -> CameraModule | None:
        result = await self.session.execute(select(CameraModule).where(
            CameraModule.camera_id == camera_id,
            CameraModule.module_id == module_id
        )
    )
        return result.scalar_one_or_none()

    async def create(
            self,
            camera_id: uuid.UUID,
            module_id: uuid.UUID,
            enabled: bool = True
    ) -> CameraModule:
        camera_module = CameraModule(
            camera_id = camera_id,
            module_id = module_id,
            enabled = enabled
        )
        self.session.add(camera_module)

        await self.session.flush()

        return camera_module

    async def delete(
            self,
            camera_module: CameraModule
    ) -> None:

        await self.session.delete(camera_module)