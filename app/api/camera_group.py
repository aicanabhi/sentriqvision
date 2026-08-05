"""
Camera Group API
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.deps import (
    get_db,
    get_current_org_admin,
    get_current_active_user,
)


from app.schemas.camera_group import (
    CameraGroupCreate,
    CameraGroupUpdate,
    CameraGroupResponse,
)


from app.services.camera_group_service import (
    CameraGroupService,
)



router = APIRouter(
    prefix="/camera-groups",
    tags=["Camera Group"]
)



@router.post(
    "",
    response_model=CameraGroupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    data: CameraGroupCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_org_admin),
):

    service = CameraGroupService(db)

    return await service.create(data)




@router.get(
    "",
    response_model=list[CameraGroupResponse],
)
async def get_groups(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_active_user),
):

    service = CameraGroupService(db)

    return await service.get_all()




@router.get(
    "/{group_id}",
    response_model=CameraGroupResponse,
)
async def get_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_active_user),
):

    service = CameraGroupService(db)

    group = await service.get_by_id(
        group_id
    )

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Camera group not found"
        )

    return group




@router.put(
    "/{group_id}",
    response_model=CameraGroupResponse,
)
async def update_group(
    group_id: UUID,
    data: CameraGroupUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_org_admin),
):

    service = CameraGroupService(db)

    group = await service.update(
        group_id,
        data
    )

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Camera group not found"
        )

    return group




@router.delete(
    "/{group_id}"
)
async def delete_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_org_admin),
):

    service = CameraGroupService(db)

    success = await service.delete(
        group_id
    )


    if not success:
        raise HTTPException(
            status_code=404,
            detail="Camera group not found"
        )


    return {
        "success": True,
        "message": "Camera group deleted successfully"
    }