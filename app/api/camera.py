"""
Camera API

Camera Management Endpoints
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_active_user,
    get_current_org_admin,
)

from app.schemas.camera import (
    CameraCreate,
    CameraUpdate,
    CameraResponse,
)

from app.services.camera_service import CameraService


router = APIRouter(
    prefix="/cameras",
    tags=["Camera"],
)


# ==========================================================
# Create Camera
# ==========================================================

@router.post(
    "",
    response_model=CameraResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_camera(
    camera: CameraCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):

    service = CameraService(db)

    return await service.create_camera(
        camera
    )


# ==========================================================
# Get All Cameras
# ==========================================================

@router.get(
    "",
    response_model=list[CameraResponse],
)
async def get_cameras(
    organization_id: UUID | None = Query(
        default=None
    ),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):

    service = CameraService(db)

    return await service.get_cameras(
        organization_id
    )


# ==========================================================
# Get Camera By ID
# ==========================================================

@router.get(
    "/{camera_id}",
    response_model=CameraResponse,
)
async def get_camera(
    camera_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):

    service = CameraService(db)

    camera = await service.get_camera(
        camera_id
    )

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera not found",
        )

    return camera


# ==========================================================
# Update Camera
# ==========================================================

@router.put(
    "/{camera_id}",
    response_model=CameraResponse,
)
async def update_camera(
    camera_id: UUID,
    camera: CameraUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):

    service = CameraService(db)

    result = await service.update_camera(
        camera_id,
        camera,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Camera not found",
        )

    return result


# ==========================================================
# Delete Camera
# ==========================================================

@router.delete(
    "/{camera_id}"
)
async def delete_camera(
    camera_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):

    service = CameraService(db)

    result = await service.delete_camera(
        camera_id
    )

    return result


# ==========================================================
# Start Camera Stream
# ==========================================================

@router.post(
    "/{camera_id}/start"
)
async def start_camera(
    camera_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):

    service = CameraService(db)

    return await service.start_stream(
        camera_id
    )


# ==========================================================
# Stop Camera Stream
# ==========================================================

@router.post(
    "/{camera_id}/stop"
)
async def stop_camera(
    camera_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):

    service = CameraService(db)

    return await service.stop_stream(
        camera_id
    )