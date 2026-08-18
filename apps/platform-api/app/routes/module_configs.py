import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.schemas.module_config import (
    ModuleConfigCreate,
    ModuleConfigUpdate,
ModuleConfigResponse,
)
from app.services.module_config import ModuleConfigService

router = APIRouter(
    prefix="/module-configs",
    tags=["module-configs"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# List all configurations
@router.get("/", response_model=list[ModuleConfigResponse])
async def list_module_configs(
        session: AsyncSession = Depends(get_db),
):
    service = ModuleConfigService(session)
    return await service.get_all()

# Get configuration by ID
@router.get("/{config_id}", response_model=ModuleConfigResponse)
async def get_module_config(
        config_id: int,
        session: AsyncSession = Depends(get_db),
):
    service = ModuleConfigService(session)
    config = await service.get_by_id(config_id)

    if config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module Configuration not found")
    return config

# Get configuration for a camera-module mapping
@router.get("/camera-module/{camera_module_id}", response_model=ModuleConfigResponse)
async def get_config_by_camera_module(
        camera_module_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = ModuleConfigService(session)

    config = await service.get_by_camera_module(camera_module_id)

    if config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module Configuration not found")
    return config

# Create configuration
@router.post("/", response_model=ModuleConfigResponse)
async def create_module_config(
        data: ModuleConfigCreate,
        session: AsyncSession = Depends(get_db),
):
    service = ModuleConfigService(session)

    try:
        config = await service.create(
            camera_module_id=data.camera_module_id,
            configuration=data.configuration,
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    await session.commit()
    await session.refresh(config)

    return config

# Update configuration
@router.put("/{config_id}", response_model=ModuleConfigResponse)
async def update_module_config(
        config_id: uuid.UUID,
        data: ModuleConfigUpdate,
        session: AsyncSession = Depends(get_db),
):
    service = ModuleConfigService(session)

    try:
        config = await service.update(
            config_id=config_id,
            configuration=data.configuration,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    await session.commit()
    await session.refresh(config)

    return config

# Delete configuration
@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module_config(
        config_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = ModuleConfigService(session)

    config = await service.get_by_id(config_id)

    if config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module Configuration not found")

    await service.delete(config_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)