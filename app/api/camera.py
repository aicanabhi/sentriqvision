"""
Camera API

Camera Management Endpoints
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
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


router = APIRouter()


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
    """
    Register a new AI camera.
    """

    service = CameraService(db)

    return await service.create_camera(
        camera
    )


# ==========================================================
# List Cameras
# ==========================================================

@router.get("")
async def list_cameras(
    page: int = Query(
        default=1,
        ge=1,
    ),

    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
    ),

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        get_current_active_user
    ),
):
    """
    Get all cameras.
    """

    service = CameraService(db)

    return await service.list_cameras(
        page,
        per_page,
    )


# ==========================================================
# Get Camera
# ==========================================================

@router.get(
    "/{camera_id}",
    response_model=CameraResponse,
)
async def get_camera(
    camera_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        get_current_active_user
    ),
):
    """
    Get camera details.
    """

    service = CameraService(db)

    return await service.get_camera(
        camera_id
    )


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

    current_user=Depends(
        get_current_org_admin
    ),
):
    """
    Update camera configuration.
    """

    service = CameraService(db)

    return await service.update_camera(
        camera_id,
        camera,
    )


# ==========================================================
# Delete Camera
# ==========================================================

@router.delete(
    "/{camera_id}"
)
async def delete_camera(
    camera_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        get_current_org_admin
    ),
):
    """
    Remove camera.
    """

    service = CameraService(db)

    await service.delete_camera(
        camera_id
    )

    return {
        "success": True,
        "message": "Camera deleted successfully",
    }


# ==========================================================
# Camera Health
# ==========================================================

@router.get(
    "/{camera_id}/health"
)
async def camera_health(
    camera_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        get_current_active_user
    ),
):
    """
    Get camera health status.
    """

    service = CameraService(db)

    return await service.get_health(
        camera_id
    )


# ==========================================================
# Start Camera Stream
# ==========================================================

@router.post(
    "/{camera_id}/start"
)
async def start_camera(
    camera_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        get_current_org_admin
    ),
):
    """
    Start RTSP/AI processing stream.
    """

    service = CameraService(db)

    return await service.start_camera(
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

    current_user=Depends(
        get_current_org_admin
    ),
):
    """
    Stop camera stream.
    """

    service = CameraService(db)

    return await service.stop_camera(
        camera_id
    )


# ==========================================================
# Camera Status
# ==========================================================

@router.get(
    "/{camera_id}/status"
)
async def camera_status(
    camera_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        get_current_active_user
    ),
):
    """
    Current camera status.
    """

    service = CameraService(db)

    return await service.get_status(
        camera_id
    )