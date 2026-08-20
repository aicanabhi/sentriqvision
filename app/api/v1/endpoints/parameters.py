import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.models.organization import Organization
from app.models.camera import Camera
from app.models.ai_parameter import ParameterCameraAssignment
from app.schemas.parameter import (
    ParameterResponse,
    ParameterToggleRequest,
    ParameterEntitlementRequest,
    ParameterConfigRequest,
)


from app.schemas.response import ResponseEnvelope
from app.services.parameter_service import ParameterService
from app.services.rbac_service import get_current_user

router = APIRouter()


async def get_user_org_id(user: User, db: AsyncSession) -> uuid.UUID:
    """Helper to extract organization_id from current user tenant."""
    query = select(Tenant).where(Tenant.id == user.tenant_id)
    res = await db.execute(query)
    tenant = res.scalar_one_or_none()
    if tenant and tenant.organization_id:
        return tenant.organization_id
    return user.tenant_id


async def check_organization_access(
    requested_org_id: Optional[uuid.UUID],
    current_user: User,
    db: AsyncSession,
) -> uuid.UUID:
    """
    Enforces tenant isolation and role-based access scoping.
    Super Admin can access requested_org_id or current_user's org.
    Non-Super Admin can ONLY access their own org_id. Attempting to access another org returns 403 Forbidden.
    """
    user_org_id = await get_user_org_id(current_user, db)
    roles = getattr(current_user, "roles", []) or []
    is_superadmin = (
        getattr(current_user, "is_superuser", False) or
        any(getattr(r, "name", "") == "SUPER_ADMIN" for r in roles)
    )

    if requested_org_id is None:
        return user_org_id

    if not is_superadmin and requested_org_id != user_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access or modify another organization's parameters."
        )
    return requested_org_id


@router.get("/", response_model=ResponseEnvelope[List[ParameterResponse]])
async def list_parameters(
    domain: Optional[str] = Query(None, description="Filter by domain"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: ENABLED/DISABLED/ALL"),
    search: Optional[str] = Query(None, description="Search term"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists organization's 54 AI parameters from PostgreSQL database."""
    org_id = await get_user_org_id(current_user, db)
    service = ParameterService(db)
    params = await service.get_organization_parameters(
        org_id=org_id,
        domain=domain,
        status=status_filter,
        search=search,
    )
    return ResponseEnvelope(success=True, data=params)


@router.get("/organization-entitlements", response_model=ResponseEnvelope[List[dict]])
@router.get("/organization", response_model=ResponseEnvelope[List[dict]])
async def list_enabled_organization_capabilities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Returns ONLY capabilities enabled for the authenticated organization (Requirement 14)."""
    org_id = await get_user_org_id(current_user, db)
    service = ParameterService(db)
    params = await service.get_organization_parameters(org_id=org_id, status="ENABLED")

    enabled_caps = [
        {
            "key": p["code"],
            "code": p["code"],
            "name": p["name"],
            "domain": p["domain"],
            "status": "ACTIVE",
            "enabled": True,
            "confidence_threshold": p["confidence_threshold"],
            "sampling_fps": p["sampling_fps"],
        }
        for p in params if p["enabled"]
    ]
    return ResponseEnvelope(success=True, data=enabled_caps)


@router.get("/catalog", response_model=ResponseEnvelope[List[dict]])
async def get_master_catalog(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gets global 54 master catalog specifications."""
    service = ParameterService(db)
    params = await service.get_catalog_items()
    data = [
        {
            "id": str(p.id),
            "service_number": p.service_number,
            "code": p.code,
            "name": p.name,
            "domain": p.domain,
            "description": p.description,
            "hardware_requirement": p.hardware_requirement,
            "processing_mode": p.processing_mode,
            "default_confidence": p.default_confidence,
            "default_fps": p.default_fps,
            "is_active": p.is_active,
        }
        for p in params
    ]
    return ResponseEnvelope(success=True, data=data)


@router.get("/organization/{org_id}", response_model=ResponseEnvelope[List[dict]])
async def get_organization_capabilities_by_id(
    org_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists organization AI capabilities by org ID."""
    try:
        requested_uuid = uuid.UUID(org_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid organization_id UUID format"
        )

    target_org_id = await check_organization_access(requested_uuid, current_user, db)

    org_exists = (await db.execute(select(Organization).where(Organization.id == target_org_id))).scalar_one_or_none()
    if not org_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization '{org_id}' not found"
        )

    service = ParameterService(db)
    params = await service.get_organization_parameters(org_id=target_org_id)
    return ResponseEnvelope(success=True, data=params)


@router.put("/{param_id}/toggle", response_model=ResponseEnvelope[dict])
@router.patch("/{param_id}/toggle", response_model=ResponseEnvelope[dict])
async def toggle_parameter(
    param_id: str,
    payload: ParameterToggleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggles Enable/Disable for a parameter in database."""
    target_org_id = await check_organization_access(payload.organization_id, current_user, db)

    roles = getattr(current_user, "roles", []) or []
    is_superadmin = (
        getattr(current_user, "is_superuser", False) or
        any(getattr(r, "name", "") == "SUPER_ADMIN" for r in roles)
    )

    service = ParameterService(db)
    try:
        result = await service.toggle_parameter(
            org_id=target_org_id,
            param_id=param_id,
            enabled=payload.enabled,
            is_superadmin=is_superadmin,
        )
        return ResponseEnvelope(success=True, data=result)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )



@router.patch("/{param_id}/entitlement", response_model=ResponseEnvelope[dict])
async def update_parameter_entitlement(
    param_id: str,
    payload: ParameterEntitlementRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Explicitly grants or revokes an AI capability entitlement for an organization."""
    target_org_id = await check_organization_access(payload.organization_id, current_user, db)

    roles = getattr(current_user, "roles", []) or []
    is_superadmin = (
        getattr(current_user, "is_superuser", False) or
        any(getattr(r, "name", "") == "SUPER_ADMIN" for r in roles)
    )

    if not is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin privileges required to manage capability entitlements."
        )

    service = ParameterService(db)
    try:
        try:
            pid = uuid.UUID(param_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid parameter ID format")

        result = await service.assign_entitlement(
            org_id=target_org_id,
            param_id=pid,
            enabled=payload.entitled,
        )
        return ResponseEnvelope(success=True, data=result)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update entitlement: {str(e)}"
        )


@router.put("/{param_id}/configure", response_model=ResponseEnvelope[dict])
async def configure_parameter(
    param_id: str,
    payload: ParameterConfigRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Saves parameter configuration settings (confidence, FPS, mode, cameras) to database."""
    target_org_id = await check_organization_access(payload.organization_id, current_user, db)

    service = ParameterService(db)
    try:
        config_data = payload.model_dump(exclude_none=True)
        result = await service.update_parameter_config(
            org_id=target_org_id,
            param_id=param_id,
            config_data=config_data,
        )
        return ResponseEnvelope(success=True, data=result)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to configure parameter: {str(e)}"
        )


@router.get("/{param_id}/cameras", response_model=ResponseEnvelope[List[dict]])
async def get_parameter_assigned_cameras(
    param_id: str,
    organization_id: Optional[uuid.UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gets assigned cameras for an AI parameter."""
    target_org_id = await check_organization_access(organization_id, current_user, db)

    try:
        pid = uuid.UUID(param_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid parameter ID format")

    query = select(ParameterCameraAssignment).where(
        ParameterCameraAssignment.organization_id == target_org_id,
        ParameterCameraAssignment.parameter_id == pid,
        ParameterCameraAssignment.enabled == True
    )
    assignments = (await db.execute(query)).scalars().all()
    assigned_cam_ids = [a.camera_id for a in assignments]

    cams_query = (
        select(Camera)
        .join(Tenant, Camera.tenant_id == Tenant.id)
        .where(Tenant.organization_id == target_org_id)
    )
    all_cams = (await db.execute(cams_query)).scalars().all()

    result = [
        {
            "camera_id": str(cam.id),
            "name": cam.name,
            "location": cam.location,
            "rtsp_url": cam.rtsp_url,
            "assigned": cam.id in assigned_cam_ids,
        }
        for cam in all_cams
    ]
    return ResponseEnvelope(success=True, data=result)
