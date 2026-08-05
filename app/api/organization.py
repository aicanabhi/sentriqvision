"""
Organization API

CRUD APIs for Organization Management.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_super_admin,
    pagination_params,
)
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)
from app.services.organization_service import OrganizationService

router = APIRouter()


# ==========================================================
# Create Organization
# ==========================================================

@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    organization: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Create a new organization.
    """

    service = OrganizationService(db)

    return await service.create_organization(organization)


# ==========================================================
# List Organizations
# ==========================================================

@router.get(
    "",
)
async def list_organizations(
    pagination=Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Get all organizations.
    """

    service = OrganizationService(db)

    return await service.list_organizations(
        page=pagination["page"],
        per_page=pagination["per_page"],
    )


# ==========================================================
# Get Organization
# ==========================================================

@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
async def get_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Get organization details.
    """

    service = OrganizationService(db)

    return await service.get_organization(organization_id)


# ==========================================================
# Update Organization
# ==========================================================

@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
async def update_organization(
    organization_id: UUID,
    organization: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Update organization.
    """

    service = OrganizationService(db)

    return await service.update_organization(
        organization_id,
        organization,
    )


# ==========================================================
# Delete Organization
# ==========================================================

@router.delete(
    "/{organization_id}",
)
async def delete_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Delete organization.
    """

    service = OrganizationService(db)

    await service.delete_organization(organization_id)

    return {
        "success": True,
        "message": "Organization deleted successfully",
    }


# ==========================================================
# Activate Organization
# ==========================================================

@router.patch(
    "/{organization_id}/activate",
)
async def activate_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Activate organization.
    """

    service = OrganizationService(db)

    return await service.activate_organization(organization_id)


# ==========================================================
# Deactivate Organization
# ==========================================================

@router.patch(
    "/{organization_id}/deactivate",
)
async def deactivate_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Deactivate organization.
    """

    service = OrganizationService(db)

    return await service.deactivate_organization(
        organization_id
    )