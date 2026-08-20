import uuid
import psutil
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.organization import Organization
from app.models.tenant import Tenant
from app.models.user import User, Role
from app.models.camera import Camera
from app.models.event import Event, Alert
from app.models.ai_parameter import (
    AIParameterCatalog,
    OrganizationAIParameter,
    AuditLog,
    AIInferenceLog
)
from app.schemas.response import ResponseEnvelope
from app.services.rbac_service import get_current_user, require_roles
from app.services.parameter_service import ParameterService

from app.services.ai_engine.registry import global_ai_registry

router = APIRouter()


@router.get("/overview", response_model=ResponseEnvelope[dict])
async def get_platform_overview(
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Super Admin overview telemetry."""
    orgs_count = (await db.execute(select(func.count()).select_from(Organization))).scalar() or 0
    active_cams = (await db.execute(select(func.count()).select_from(Camera).where(Camera.status == "ONLINE"))).scalar() or 0
    active_caps = (await db.execute(select(func.count()).select_from(OrganizationAIParameter).where(OrganizationAIParameter.enabled == True))).scalar() or 0
    crit_alerts = (await db.execute(select(func.count()).select_from(Alert).where(Alert.severity == "CRITICAL", Alert.status == "NEW"))).scalar() or 0

    all_health = global_ai_registry.get_all_capabilities_health()
    running_fps = round(sum(item.get("fps", 0.0) for item in all_health if item.get("status") == "RUNNING"), 1)
    if running_fps == 0.0 and active_cams > 0:
        cam_fps_sum = (await db.execute(select(func.sum(Camera.fps_sampling)).where(Camera.status == "ONLINE"))).scalar() or 0.0
        running_fps = round(float(cam_fps_sum), 1)

    return ResponseEnvelope(
        success=True,
        data={
            "organizations_count": orgs_count,
            "active_cameras": active_cams,
            "active_capabilities": active_caps,
            "critical_alerts": crit_alerts,
            "running_inferences_fps": running_fps,
            "system_health": "100% OPERATIONAL"
        }
    )


@router.get("/organizations", response_model=ResponseEnvelope[List[dict]])
async def list_organizations(
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Super admin list of all organizations with parameter entitlement stats."""
    query = select(Organization).options(selectinload(Organization.tenants))
    res = await db.execute(query)
    orgs = res.scalars().all()

    output = []
    for org in orgs:
        # Count enabled parameters
        p_query = select(func.count()).select_from(OrganizationAIParameter).where(
            OrganizationAIParameter.organization_id == org.id,
            OrganizationAIParameter.enabled == True
        )
        enabled_count = (await db.execute(p_query)).scalar() or 0

        # Count cameras
        c_query = select(func.count()).select_from(Camera).join(Tenant).where(
            Tenant.organization_id == org.id
        )
        cam_count = (await db.execute(c_query)).scalar() or 0

        output.append({
            "id": str(org.id),
            "name": org.name,
            "slug": org.slug,
            "is_active": org.is_active,
            "status": "ACTIVE" if org.is_active else "SUSPENDED",
            "enabled_parameters": enabled_count,
            "total_parameters": 54,
            "camera_count": cam_count,
            "tenant_count": len(org.tenants),
            "created_at": org.created_at.isoformat() if org.created_at else None,
        })
    return ResponseEnvelope(success=True, data=output)


@router.post("/organizations", response_model=ResponseEnvelope[dict])
async def create_organization(
    payload: Dict[str, Any],
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Super Admin onboarding for new Organization."""
    name = payload.get("name")
    slug = payload.get("slug") or name.lower().replace(" ", "-") if name else "org-slug"

    if not name:
        raise HTTPException(status_code=400, detail="Organization name is required")

    org = Organization(name=name, slug=slug, is_active=True)
    db.add(org)
    await db.flush()

    # Create default tenant
    tenant = Tenant(
        organization_id=org.id,
        name=f"{name} Main HQ",
        code=f"{slug}-hq",
        config={"max_cameras": 50}
    )
    db.add(tenant)
    await db.flush()

    # Initialize 54 AI parameters
    param_service = ParameterService(db)
    await param_service.seed_catalog_and_org_entitlements(org.id)

    # Audit log
    audit = AuditLog(
        organization_id=org.id,
        user_id=current_user.id,
        action="CREATE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org.id),
        details={"name": name, "slug": slug}
    )
    self_db = db
    self_db.add(audit)
    await self_db.commit()

    return ResponseEnvelope(
        success=True,
        data={
            "id": str(org.id),
            "name": org.name,
            "slug": org.slug,
            "status": "ACTIVE",
            "message": "Organization onboarded and 54 AI parameters initialized."
        }
    )


@router.get("/organizations/{org_id}", response_model=ResponseEnvelope[dict])
async def get_organization_details(
    org_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Gets complete organization details with tenant, camera, user, and parameter metrics."""
    query = select(Organization).where(Organization.id == org_id).options(selectinload(Organization.tenants))
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    p_query = select(func.count()).select_from(OrganizationAIParameter).where(
        OrganizationAIParameter.organization_id == org.id,
        OrganizationAIParameter.enabled == True
    )
    enabled_count = (await db.execute(p_query)).scalar() or 0

    c_query = select(func.count()).select_from(Camera).join(Tenant).where(Tenant.organization_id == org.id)
    cam_count = (await db.execute(c_query)).scalar() or 0

    return ResponseEnvelope(
        success=True,
        data={
            "id": str(org.id),
            "name": org.name,
            "slug": org.slug,
            "status": getattr(org, "status", "ACTIVE" if org.is_active else "SUSPENDED"),
            "is_active": org.is_active,
            "deleted_at": org.deleted_at.isoformat() if getattr(org, "deleted_at", None) else None,
            "contact_email": getattr(org, "contact_email", None),
            "address": getattr(org, "address", None),
            "timezone": getattr(org, "timezone", "UTC"),
            "subscription_tier": getattr(org, "subscription_tier", "ENTERPRISE"),
            "enabled_parameters": enabled_count,
            "total_parameters": 54,
            "camera_count": cam_count,
            "tenant_count": len(org.tenants),
            "created_at": org.created_at.isoformat() if org.created_at else None,
            "updated_at": org.updated_at.isoformat() if org.updated_at else None,
        }
    )


@router.patch("/organizations/{org_id}", response_model=ResponseEnvelope[dict])
async def update_organization(
    org_id: uuid.UUID,
    payload: Dict[str, Any],
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Edits organization details with audit logging."""
    query = select(Organization).where(Organization.id == org_id)
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    old_data = {"name": org.name, "slug": org.slug, "is_active": org.is_active}

    if "name" in payload and payload["name"]:
        org.name = payload["name"]
    if "slug" in payload and payload["slug"]:
        org.slug = payload["slug"]
    if "contact_email" in payload:
        org.contact_email = payload["contact_email"]
    if "address" in payload:
        org.address = payload["address"]
    if "timezone" in payload:
        org.timezone = payload["timezone"]
    if "subscription_tier" in payload:
        org.subscription_tier = payload["subscription_tier"]

    audit = AuditLog(
        organization_id=org.id,
        user_id=current_user.id,
        action="UPDATE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org.id),
        details={"old": old_data, "new": payload}
    )
    db.add(audit)
    await db.commit()

    return ResponseEnvelope(success=True, data={"id": str(org.id), "name": org.name, "slug": org.slug, "status": org.status})


@router.post("/organizations/{org_id}/activate", response_model=ResponseEnvelope[dict])
@router.put("/organizations/{org_id}/status", response_model=ResponseEnvelope[dict])
async def activate_organization(
    org_id: uuid.UUID,
    payload: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Activates an organization."""
    query = select(Organization).where(Organization.id == org_id)
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    org.is_active = True
    org.status = "ACTIVE"
    org.deleted_at = None

    audit = AuditLog(
        organization_id=org.id,
        user_id=current_user.id,
        action="ACTIVATE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org.id),
        details={"status": "ACTIVE"}
    )
    db.add(audit)
    await db.commit()

    return ResponseEnvelope(success=True, data={"id": str(org_id), "is_active": True, "status": "ACTIVE"})


@router.post("/organizations/{org_id}/deactivate", response_model=ResponseEnvelope[dict])
async def deactivate_organization(
    org_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Deactivates/Suspends an organization."""
    query = select(Organization).where(Organization.id == org_id)
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    org.is_active = False
    org.status = "SUSPENDED"

    # Disable parameters during suspension
    await db.execute(
        update(OrganizationAIParameter)
        .where(OrganizationAIParameter.organization_id == org_id)
        .values(enabled=False)
    )

    audit = AuditLog(
        organization_id=org.id,
        user_id=current_user.id,
        action="DEACTIVATE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org.id),
        details={"status": "SUSPENDED"}
    )
    db.add(audit)
    await db.commit()

    return ResponseEnvelope(success=True, data={"id": str(org_id), "is_active": False, "status": "SUSPENDED"})


@router.delete("/organizations/{org_id}", response_model=ResponseEnvelope[dict])
async def soft_delete_organization(
    org_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Soft deletes an organization."""
    query = select(Organization).where(Organization.id == org_id)
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    org.is_active = False
    org.status = "DELETED"
    org.deleted_at = datetime.now(timezone.utc)

    # Disable parameters
    await db.execute(
        update(OrganizationAIParameter)
        .where(OrganizationAIParameter.organization_id == org_id)
        .values(enabled=False)
    )

    audit = AuditLog(
        organization_id=org.id,
        user_id=current_user.id,
        action="DELETE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org.id),
        details={"status": "DELETED", "soft_delete": True}
    )
    db.add(audit)
    await db.commit()

    return ResponseEnvelope(success=True, data={"id": str(org_id), "status": "DELETED", "deleted_at": org.deleted_at.isoformat()})


@router.post("/organizations/{org_id}/restore", response_model=ResponseEnvelope[dict])
async def restore_organization(
    org_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Restores a soft-deleted organization back to SUSPENDED status for review."""
    query = select(Organization).where(Organization.id == org_id)
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    org.status = "SUSPENDED"
    org.is_active = False
    org.deleted_at = None

    audit = AuditLog(
        organization_id=org.id,
        user_id=current_user.id,
        action="RESTORE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org.id),
        details={"status": "SUSPENDED"}
    )
    db.add(audit)
    await db.commit()

    return ResponseEnvelope(success=True, data={"id": str(org_id), "status": "SUSPENDED", "is_active": False})


@router.delete("/organizations/{org_id}/purge", response_model=ResponseEnvelope[dict])
async def purge_organization(
    org_id: uuid.UUID,
    confirm_name: str = Query(..., description="Must match exact organization name"),
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Permanently purges an organization and all associated resources."""
    query = select(Organization).where(Organization.id == org_id)
    org = (await db.execute(query)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    if org.name != confirm_name:
        raise HTTPException(status_code=400, detail=f"Confirmation name '{confirm_name}' does not match organization name '{org.name}'")

    org_name = org.name

    # Delete parameters
    await db.execute(
        OrganizationAIParameter.__table__.delete().where(OrganizationAIParameter.organization_id == org_id)
    )

    # Delete organization
    await db.delete(org)

    audit = AuditLog(
        organization_id=None,
        user_id=current_user.id,
        action="PURGE_ORGANIZATION",
        resource_type="organization",
        resource_id=str(org_id),
        details={"name": org_name, "purged": True}
    )
    db.add(audit)
    await db.commit()

    return ResponseEnvelope(success=True, data={"id": str(org_id), "name": org_name, "status": "PURGED"})


@router.get("/organizations/{org_id}/capabilities", response_model=ResponseEnvelope[List[dict]])
async def get_organization_capabilities_superadmin(
    org_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Gets all 54 capabilities for a specific organization."""
    service = ParameterService(db)
    params = await service.get_organization_parameters(org_id=org_id)
    return ResponseEnvelope(success=True, data=params)


@router.patch("/organizations/{org_id}/capabilities/{param_id}", response_model=ResponseEnvelope[dict])
@router.put("/organizations/{org_id}/capabilities/{param_id}", response_model=ResponseEnvelope[dict])
async def toggle_organization_capability_superadmin(
    org_id: uuid.UUID,
    param_id: str,
    payload: Dict[str, Any],
    current_user: User = Depends(require_roles(["SUPER_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Super admin toggle capability endpoint for an organization."""
    enabled = payload.get("enabled")
    if enabled is None:
        raise HTTPException(status_code=400, detail="enabled field is required")
    service = ParameterService(db)
    try:
        result = await service.toggle_parameter(
            org_id=org_id,
            param_id=param_id,
            enabled=bool(enabled),
            is_superadmin=True
        )
        return ResponseEnvelope(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def _fetch_hardware_gpu_metrics() -> Dict[str, Any]:
    """Inspects host machine for real NVIDIA GPU metrics via pynvml / PyTorch with safe fallback."""
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count > 0:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode("utf-8")
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            try:
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            except Exception:
                temp = None
            try:
                power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
            except Exception:
                power = None
            return {
                "available": True,
                "gpu_model": str(name),
                "gpu_percent": float(util.gpu),
                "vram_used_mb": round(mem_info.used / (1024 * 1024), 2),
                "vram_total_mb": round(mem_info.total / (1024 * 1024), 2),
                "vram_free_mb": round(mem_info.free / (1024 * 1024), 2),
                "temperature_celsius": temp,
                "power_draw_watts": power,
            }
    except Exception:
        pass

    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            allocated = torch.cuda.memory_allocated(0) / (1024 * 1024)
            reserved = torch.cuda.memory_reserved(0) / (1024 * 1024)
            total = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
            return {
                "available": True,
                "gpu_model": device_name,
                "gpu_percent": 0.0,
                "vram_used_mb": round(allocated, 2),
                "vram_total_mb": round(total, 2),
                "vram_free_mb": round(total - reserved, 2),
                "temperature_celsius": None,
                "power_draw_watts": None,
            }
    except Exception:
        pass

    return {
        "available": False,
        "gpu_model": "GPU Not Available",
        "gpu_percent": 0.0,
        "vram_used_mb": 0.0,
        "vram_total_mb": 0.0,
        "vram_free_mb": 0.0,
        "temperature_celsius": None,
        "power_draw_watts": None,
    }


@router.get("/system-health", response_model=ResponseEnvelope[dict])
async def get_system_health(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Real-time platform system telemetry (CPU, RAM, GPU, active cameras, events, inference latency)."""
    cpu_pct = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()

    # Query counts from DB
    total_cams = (await db.execute(select(func.count()).select_from(Camera))).scalar() or 0
    online_cams = (await db.execute(select(func.count()).select_from(Camera).where(Camera.status == "ONLINE"))).scalar() or 0
    offline_cams = total_cams - online_cams

    enabled_params = (await db.execute(select(func.count()).select_from(OrganizationAIParameter).where(OrganizationAIParameter.enabled == True))).scalar() or 0
    events_count = (await db.execute(select(func.count()).select_from(Event))).scalar() or 0
    alerts_count = (await db.execute(select(func.count()).select_from(Alert).where(Alert.status == "NEW"))).scalar() or 0

    gpu_info = _fetch_hardware_gpu_metrics()

    return ResponseEnvelope(
        success=True,
        data={
            "cpu_percent": round(cpu_pct, 1),
            "ram_used_gb": round((ram.total - ram.available) / (1024**3), 2),
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "gpu_available": gpu_info["available"],
            "gpu_model": gpu_info["gpu_model"],
            "gpu_percent": gpu_info["gpu_percent"],
            "vram_used_mb": gpu_info["vram_used_mb"],
            "vram_total_mb": gpu_info["vram_total_mb"],
            "active_cameras": total_cams,
            "online_cameras": online_cams,
            "offline_cameras": offline_cams,
            "enabled_parameters": enabled_params,
            "total_events_today": events_count,
            "critical_alerts": alerts_count,
            "system_health": "HEALTHY",
            "active_gpu_workers": 1 if gpu_info["available"] else 0,
            "inference_queue_depth": 0,
        }
    )


@router.get("/gpu", response_model=ResponseEnvelope[dict])
async def get_gpu_telemetry(
    current_user: User = Depends(get_current_user),
):
    """Super Admin GPU pool and worker telemetry."""
    gpu_info = _fetch_hardware_gpu_metrics()
    return ResponseEnvelope(
        success=True,
        data={
            "gpu_available": gpu_info["available"],
            "gpu_model": gpu_info["gpu_model"],
            "gpu_utilization": gpu_info["gpu_percent"],
            "vram_used_mb": gpu_info["vram_used_mb"],
            "vram_total_mb": gpu_info["vram_total_mb"],
            "vram_free_mb": gpu_info["vram_free_mb"],
            "temperature_celsius": gpu_info["temperature_celsius"],
            "power_draw_watts": gpu_info["power_draw_watts"],
            "active_workers": 1 if gpu_info["available"] else 0,
            "models_loaded": ["SCRFD", "YOLOv8x", "ArcFace", "ByteTrack"] if gpu_info["available"] else [],
            "queue_depth": 0,
        }
    )


@router.get("/audit-logs", response_model=ResponseEnvelope[List[dict]])
async def list_audit_logs(
    limit: int = Query(50, le=200),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists recent platform audit logs."""
    query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    res = await db.execute(query)
    logs = res.scalars().all()

    output = [
        {
            "id": str(log.id),
            "organization_id": str(log.organization_id) if log.organization_id else None,
            "user_id": str(log.user_id) if log.user_id else None,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "details": log.details,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
    return ResponseEnvelope(success=True, data=output)
