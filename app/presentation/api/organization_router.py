
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.schemas.organization import OrganizationUpdate, OrganizationResponse
from app.application.schemas.common import APIResponse
from app.application.services.organization_service import OrganizationService
from app.infrastructure.utils.dependencies import (
    get_db,
    get_admin_or_super_admin
)

router = APIRouter(prefix="/organization", tags=["Organization"])


@router.get("/profile", response_model=APIResponse[OrganizationResponse])
async def get_organization_profile(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_admin_or_super_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = OrganizationService(db)
    org = await service.get_organization_by_id(current_user["organization_id"])
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=org)


@router.put("/profile", response_model=APIResponse[OrganizationResponse])
async def update_organization_profile(
    request: OrganizationUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
  current_user = Depends(get_admin_or_super_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = OrganizationService(db)
    org = await service.update_organization(
        current_user["organization_id"],
        request,
        current_user["id"]
    )
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=org)
