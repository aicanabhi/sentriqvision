import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.schemas.module import ModuleCreate, ModuleResponse
from app.services.module import ModuleService

router = APIRouter(
    prefix="/modules",
    tags=["modules"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# List all modules
@router.get("/", response_model=list[ModuleResponse])
async def list_modules(session: AsyncSession = Depends(get_db)):
    service = ModuleService(session)
    return await service.get_all()

# Get module by ID
@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(module_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = ModuleService(session)
    module = await service.get_by_id(module_id)

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

# Create module
@router.post("/", response_model=ModuleResponse)
async def create_module(data: ModuleCreate, session: AsyncSession = Depends(get_db)):
    service = ModuleService(session)

    try:
        module = await service.create(
            code=data.code,
            name=data.name,
            description=data.description,
            enabled=data.enabled,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    await session.commit()
    await session.refresh(module)
    return module

# Delete module
@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(module_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = ModuleService(session)
    module = await service.get_by_id(module_id)

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    await session.delete(module_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)