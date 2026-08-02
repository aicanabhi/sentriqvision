"""
Service API

Manages AI services available in SentriqVision platform.
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.deps import (
    get_db,
    get_current_super_admin,
    get_current_org_admin,
)

from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
)

from app.services.service_service import ServiceService


router = APIRouter()


# ==========================================================
# Create Service
# ==========================================================


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    service: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Create new platform service.
    """

    service_manager = ServiceService(db)

    return await service_manager.create_service(
        service
    )


# ==========================================================
# List Services
# ==========================================================


@router.get(
    "",
    response_model=list[ServiceResponse],
)
async def list_services(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Get all available services.
    """

    service_manager = ServiceService(db)

    return await service_manager.list_services()


# ==========================================================
# Get Service
# ==========================================================


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
async def get_service(
    service_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Get service details.
    """

    service_manager = ServiceService(db)

    return await service_manager.get_service(
        service_id
    )


# ==========================================================
# Update Service
# ==========================================================


@router.put(
    "/{service_id}",
    response_model=ServiceResponse,
)
async def update_service(
    service_id: UUID,
    service: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Update platform service.
    """

    service_manager = ServiceService(db)

    return await service_manager.update_service(
        service_id,
        service,
    )


# ==========================================================
# Delete Service
# ==========================================================


@router.delete(
    "/{service_id}",
)
async def delete_service(
    service_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Delete service.
    """

    service_manager = ServiceService(db)

    await service_manager.delete_service(
        service_id
    )

    return {
        "success": True,
        "message": "Service deleted successfully",
    }


# ==========================================================
# Enable Service For Organization
# ==========================================================


@router.post(
    "/{service_id}/enable/{organization_id}",
)
async def enable_service(
    service_id: UUID,
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Enable service for organization.
    """

    service_manager = ServiceService(db)

    return await service_manager.enable_service(
        service_id,
        organization_id,
    )


# ==========================================================
# Disable Service For Organization
# ==========================================================


@router.delete(
    "/{service_id}/disable/{organization_id}",
)
async def disable_service(
    service_id: UUID,
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Disable service for organization.
    """

    service_manager = ServiceService(db)

    return await service_manager.disable_service(
        service_id,
        organization_id,
    )


# ==========================================================
# Organization Enabled Services
# ==========================================================


@router.get(
    "/organization/{organization_id}",
)
async def organization_services(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Get services enabled for organization.
    """

    service_manager = ServiceService(db)

    return await service_manager.get_organization_services(
        organization_id
    )