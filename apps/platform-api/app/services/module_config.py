import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.module_config import ModuleConfig
from app.repositories.module_config import ModuleConfigRepository

class ModuleConfigService:
    def __init__(self, session: AsyncSession):
        self.repository = ModuleConfigRepository(session)

    async def get_by_id(self, config_id: uuid.UUID) -> ModuleConfig | None:
        return await self.repository.get_by_id(config_id)

    async def get_by_camera_module(self, camera_module_id: uuid.UUID) -> ModuleConfig | None:
        return await self.repository.get_by_camera_module(camera_module_id)

    async def get_all(self) -> list[ModuleConfig]:
        return await self.repository.get_all()

    async def create(self, camera_module_id: uuid.UUID, configuration: dict) -> ModuleConfig:
        if not isinstance(configuration, dict):
            raise ValueError("configuration must be a JSON object")

        existing = await self.repository.get_by_camera_module(camera_module_id)

        if existing is not None:
            raise ValueError("configuration already exists")

        return await self.repository.create(camera_module_id=camera_module_id, configuration=configuration)

    async def update(self, config_id: uuid.UUID, configuration: dict) -> ModuleConfig:
        if not isinstance(configuration, dict):
            raise ValueError("configuration must be a JSON object")
        config = await self.repository.get_by_id(config_id)

        if config is None:
            raise ValueError("Module configuration does not exist")

        return await self.repository.update(config=config, configuration=configuration)

    async def delete(self, config_id: uuid.UUID) -> None:
        config = await self.repository.get_by_id(config_id)
        if config is None:
            raise ValueError("Module configuration does not exist")

        await self.repository.delete(config)