import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.module import Module
from app.repositories.module import ModuleRepository

class ModuleService:
    def __init__(self, session: AsyncSession):
        self.repository = ModuleRepository(session)

    async def get_by_id(self, module_id: uuid.UUID) -> Module | None:
        return await self.repository.get_by_id(module_id)

    async def get_by_code(self, code: str) -> Module | None:
        return await self.repository.get_by_code(code)

    async def get_all(self) -> list[Module | None]:
        return await self.repository.get_all()

    async def create(
            self,
            code: str,
            name: str,
            description: str | None = None,
            enabled: bool = True
    ) -> Module:
        code = code.strip().upper()
        name = name.strip()

        if not code:
            raise ValueError("Module code cannot be empty")

        if not name:
            raise ValueError("Module name cannot be empty")

        existing = await self.repository.get_by_code(code)

        if existing is not None:
            raise ValueError("Module with code '{code}' already exists")

        return await self.repository.create(
            code=code,
            name=name,
            description=description,
            enabled=enabled
        )

    async def delete(self, module_id: uuid.UUID) -> None:
        module = await self.repository.get_by_id(module_id)

        if module is None:
            raise ValueError("Module not found")

        await self.repository.delete(module)