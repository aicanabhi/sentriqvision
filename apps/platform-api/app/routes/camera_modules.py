import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.schemas.camera_module import CameraModuleCreate, CameraModuleResponse
from app.services.camera_module import CameraModuleService

router = APIRouter(
    prefix="/camera-modules",
    tags=["camera-modules"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# List all camera-module mappings
@router.get("/", response_model=list[CameraModuleResponse])
async def list_camera_modules(session: AsyncSession = Depends(get_db)):
    service = CameraModuleService(session)
    return await service.get_all()

# List modules assigned to a camera
@router.get("/camera/{camera_id}", response_model=list[CameraModuleResponse])
async def list_camera_modules_by_camera(
        camera_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    service = CameraModuleService(session)
    return await service.get_by_camera(camera_id)

# List cameras assigned to a module
@router.get("/module/{module_id}", response_model=list[CameraModuleResponse])
async def list_camera_modules_by_module(
        module_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraModuleService(session)
    return await service.get_by_module(module_id)

# Get one mapping
@router.get("/camera_module_id", response_model=CameraModuleResponse)
async def get_camera_module(
        camera_module_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraModuleService(session)
    camera_module = await service.get_by_id(camera_module_id)

    if camera_module is None:
        raise HTTPException(status_code=404, detail="Camera module mapping not found")
    return camera_module

# Create mapping
@router.post("/", response_model=CameraModuleResponse)
async def create_camera_module(
        data: CameraModuleCreate,
        session: AsyncSession = Depends(get_db),
):
    service = CameraModuleService(session)

    try:
        camera_module = await service.create(
            camera_id=data.camera_id,
            module_id=data.module_id,
            enabled=data.enabled,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    await session.commit()
    await session.refresh(camera_module)

    return camera_module

# Delete mapping
@router.delete("/{camera_module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera_module(
        camera_module_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraModuleService(session)

    camera_module = await service.get_by_id(camera_module_id)

    if camera_module is None:
        raise HTTPException(status_code=404, detail="Camera module mapping not found")

    await service.delete(camera_module_id)

    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)