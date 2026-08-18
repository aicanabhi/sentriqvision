import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.module import Module

class ModuleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, module_id: uuid.UUID) -> Module | None:
        result = await self.session.execute(select(Module).where(Module.id == module_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Module | None:
        result = await self.session.execute(select(Module).where(Module.code == code))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Module]:
        result = await self.session.execute(select(Module).order_by(Module.name))
        return list(result.scalars().all())

    async def create(
            self,
            code: str,
            name: str,
            description: str | None = None,
            enabled: bool = True
    ) -> Module:
        module = Module(
            code=code,
            name=name,
            description=description,
            enabled=enabled
        )

        self.session.add(module)
        await self.session.flush()

        return module

    async def delete(self, module: Module) -> None:
        await self.session.delete(module)