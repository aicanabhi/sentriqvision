
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.schemas.organization import (
    OrganizationCreate, OrganizationUpdate, OrganizationResponse
)
from app.application.schemas.organization_admin import (
    OrganizationAdminCreate, OrganizationAdminResponse
)
from app.application.schemas.common import APIResponse
from app.application.services.organization_service import OrganizationService
from app.infrastructure.utils.dependencies import get_db, get_super_admin

router = APIRouter(prefix="/super-admin", tags=["Super Admin"])


@router.post("/organizations", response_model=APIResponse[OrganizationResponse])
async def create_organization(
    request: OrganizationCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    org = await service.create_organization(request, current_user["id"])
    return APIResponse(
        success=True,
        message="Organization created successfully",
        data=org
    )


@router.get("/organizations", response_model=APIResponse[List[OrganizationResponse]])
async def get_all_organizations(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    orgs = await service.get_all_organizations()
    return APIResponse(success=True, data=orgs)


@router.get("/organizations/{org_id}", response_model=APIResponse[OrganizationResponse])
async def get_organization(
    org_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    org = await service.get_organization_by_id(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return APIResponse(success=True, data=org)


@router.put("/organizations/{org_id}", response_model=APIResponse[OrganizationResponse])
async def update_organization(
    org_id: str,
    request: OrganizationUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    org = await service.update_organization(org_id, request, current_user["id"])
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return APIResponse(success=True, message="Organization updated", data=org)


@router.delete("/organizations/{org_id}")
async def delete_organization(
    org_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    success = await service.delete_organization(org_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return APIResponse(success=True, message="Organization deleted")


@router.patch("/organizations/{org_id}/activate", response_model=APIResponse[OrganizationResponse])
async def activate_organization(
    org_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    org = await service.activate_organization(org_id, current_user["id"])
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return APIResponse(success=True, message="Organization activated", data=org)


@router.patch("/organizations/{org_id}/suspend", response_model=APIResponse[OrganizationResponse])
async def suspend_organization(
    org_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    org = await service.suspend_organization(org_id, current_user["id"])
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return APIResponse(success=True, message="Organization suspended", data=org)


@router.post("/organizations/{org_id}/organization-admin", response_model=APIResponse[OrganizationAdminResponse])
async def create_organization_admin(
    org_id: str,
    request: OrganizationAdminCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    admin = await service.create_organization_admin(org_id, request, current_user["id"])
    return APIResponse(
        success=True,
        message="Organization admin created successfully",
        data=admin
    )


@router.put("/organization-admin/{admin_id}/reset-password")
async def reset_organization_admin_password(
    admin_id: str,
    new_password: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_super_admin)
):
    service = OrganizationService(db)
    await service.reset_organization_admin_password(admin_id, new_password, current_user["id"])
    return APIResponse(success=True, message="Password reset successful")


@router.get("/dashboard")
async def get_super_admin_dashboard(current_user = Depends(get_super_admin)):
    return APIResponse(
        success=True,
        data={
            "message": "Super Admin Dashboard"
        }
    )


@router.get("/platform-analytics")
async def get_platform_analytics(current_user = Depends(get_super_admin)):
    return APIResponse(
        success=True,
        data={
            "message": "Platform Analytics"
        }
    )
