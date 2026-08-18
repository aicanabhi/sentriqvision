import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.module_config import ModuleConfig

class ModuleConfigRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, config_id: uuid.UUID) -> ModuleConfig | None:
        result = await self.session.execute(select(ModuleConfig).where(ModuleConfig.id == config_id))
        return result.scalar_one_or_none()

    async def get_by_camera_module(self, camera_module_id: uuid.UUID) -> ModuleConfig | None:
        result = await self.session.execute(select(ModuleConfig).where(ModuleConfig.camera_module_id == camera_module_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModuleConfig]:
        result = await self.session.execute(select(ModuleConfig).order_by(ModuleConfig.created_at))
        return list(result.scalars().all())

    async def create(self, camera_module_id: uuid.UUID, configuration: dict) -> ModuleConfig:
        config = ModuleConfig(
        camera_module_id=camera_module_id,
        configuration=configuration
        )
        self.session.add(config)
        await self.session.commit()

        return config

    async def update(self, config: ModuleConfig, configuration: dict) -> ModuleConfig:
        config.configuration = configuration

        await self.session.flush()
        return config

    async def delete(self, config: ModuleConfig) -> None:
        await self.session.delete(config)