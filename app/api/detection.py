"""
Detection API

AI Detection Event Management
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
    pagination_params,
)

from app.schemas.detection import (
    DetectionCreate,
    DetectionResponse,
)

from app.services.detection_service import DetectionService


router = APIRouter()



# ==========================================================
# Create Detection
# ==========================================================

@router.post(
    "",
    response_model=DetectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_detection(
    detection: DetectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create AI detection event.

    Used by:
    - AI Engine
    - Camera Stream Worker
    - Object Detection Pipeline
    """

    service = DetectionService(db)

    return await service.create_detection(
        detection
    )



# ==========================================================
# List Detections
# ==========================================================

@router.get("")
async def list_detections(
    pagination=Depends(pagination_params),

    camera_id: UUID | None = None,

    detection_type: str | None = None,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_active_user),
):
    """
    Get detection events.
    """

    service = DetectionService(db)


    return await service.list_detections(

        page=pagination["page"],

        per_page=pagination["per_page"],

        camera_id=camera_id,

        detection_type=detection_type,

    )



# ==========================================================
# Get Detection
# ==========================================================

@router.get(
    "/{detection_id}",
    response_model=DetectionResponse,
)
async def get_detection(

    detection_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_active_user),

):
    """
    Get detection details.
    """

    service = DetectionService(db)


    return await service.get_detection(
        detection_id
    )



# ==========================================================
# Camera Detections
# ==========================================================

@router.get(
    "/camera/{camera_id}"
)
async def camera_detections(

    camera_id: UUID,

    limit: int = Query(
        50,
        ge=1,
        le=500,
    ),

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_active_user),

):
    """
    Get detections from specific camera.
    """

    service = DetectionService(db)


    return await service.get_camera_detections(

        camera_id,

        limit

    )



# ==========================================================
# Detection Statistics
# ==========================================================

@router.get(
    "/stats/summary"
)
async def detection_statistics(

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_active_user),

):
    """
    Detection analytics.

    Example:
    {
        person: 1200,
        vehicle: 500,
        unauthorized_access: 20
    }
    """

    service = DetectionService(db)


    return await service.get_statistics()



# ==========================================================
# Delete Detection
# ==========================================================

@router.delete(
    "/{detection_id}"
)
async def delete_detection(

    detection_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_active_user),

):

    """
    Delete detection record.
    """

    service = DetectionService(db)


    await service.delete_detection(
        detection_id
    )


    return {

        "success": True,

        "message":
        "Detection deleted successfully"

    }