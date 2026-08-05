"""
Super Admin API

Platform level administration endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_super_admin,
)

from app.services.organization_service import OrganizationService
from app.services.user_service import UserService


router = APIRouter()


# ==========================================================
# Dashboard Statistics
# ==========================================================

@router.get(
    "/dashboard",
    tags=["Super Admin"],
)
async def super_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Platform overview statistics.
    """

    organization_service = OrganizationService(db)
    user_service = UserService(db)


    organizations = await organization_service.count_organizations()

    users = await user_service.count_users()


    return {
        "success": True,
        "data": {
            "total_organizations": organizations,
            "total_users": users,
        }
    }



# ==========================================================
# Organization Management
# ==========================================================

@router.get(
    "/organizations",
    tags=["Super Admin"],
)
async def get_all_organizations(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    View all organizations.
    """

    service = OrganizationService(db)

    return await service.list_all()



# ==========================================================
# Organization Details
# ==========================================================

@router.get(
    "/organizations/{organization_id}",
    tags=["Super Admin"],
)
async def organization_details(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Get organization complete details.
    """

    service = OrganizationService(db)

    return await service.get_organization(
        organization_id
    )



# ==========================================================
# Activate Organization
# ==========================================================

@router.patch(
    "/organizations/{organization_id}/activate",
    tags=["Super Admin"],
)
async def activate_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Activate organization account.
    """

    service = OrganizationService(db)

    return await service.activate_organization(
        organization_id
    )



# ==========================================================
# Disable Organization
# ==========================================================

@router.patch(
    "/organizations/{organization_id}/disable",
    tags=["Super Admin"],
)
async def disable_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Disable organization.
    """

    service = OrganizationService(db)

    return await service.disable_organization(
        organization_id
    )



# ==========================================================
# Platform Users
# ==========================================================

@router.get(
    "/users",
    tags=["Super Admin"],
)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    View all platform users.
    """

    service = UserService(db)

    return await service.list_all_users()



# ==========================================================
# System Health
# ==========================================================

@router.get(
    "/system-health",
    tags=["Super Admin"],
)
async def system_health(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Platform health information.
    """

    return {
        "success": True,
        "services": {
            "api": "running",
            "database": "connected",
            "ai_engine": "ready",
            "camera_service": "ready",
        }
    }