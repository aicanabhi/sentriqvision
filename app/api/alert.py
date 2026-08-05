"""
Alert API

Handles AI generated alerts and incident management.
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
    pagination_params,
)

from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
)

from app.services.alert_service import AlertService


router = APIRouter()


# ==========================================================
# Create Alert
# ==========================================================


@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_alert(
    alert: AlertCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new alert.

    Usually created automatically by AI detection engine.
    """

    service = AlertService(db)

    return await service.create_alert(alert)



# ==========================================================
# List Alerts
# ==========================================================


@router.get("")
async def list_alerts(
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    status: str | None = None,
    severity: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get alerts with filters.

    Filters:
    - status
    - severity
    """

    service = AlertService(db)

    return await service.list_alerts(
        page=page,
        per_page=per_page,
        status=status,
        severity=severity,
    )



# ==========================================================
# Get Alert
# ==========================================================


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
async def get_alert(
    alert_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get alert details.
    """

    service = AlertService(db)

    return await service.get_alert(alert_id)



# ==========================================================
# Update Alert
# ==========================================================


@router.put(
    "/{alert_id}",
    response_model=AlertResponse,
)
async def update_alert(
    alert_id: UUID,
    alert: AlertUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Update alert information.
    """

    service = AlertService(db)

    return await service.update_alert(
        alert_id,
        alert,
    )



# ==========================================================
# Acknowledge Alert
# ==========================================================


@router.patch(
    "/{alert_id}/acknowledge",
)
async def acknowledge_alert(
    alert_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Mark alert as acknowledged.
    """

    service = AlertService(db)

    return await service.acknowledge_alert(
        alert_id,
        current_user["id"],
    )



# ==========================================================
# Resolve Alert
# ==========================================================


@router.patch(
    "/{alert_id}/resolve",
)
async def resolve_alert(
    alert_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Resolve an alert.
    """

    service = AlertService(db)

    return await service.resolve_alert(
        alert_id,
        current_user["id"],
    )



# ==========================================================
# Assign Alert
# ==========================================================


@router.patch(
    "/{alert_id}/assign/{user_id}",
)
async def assign_alert(
    alert_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Assign alert to user/team member.
    """

    service = AlertService(db)

    return await service.assign_alert(
        alert_id,
        user_id,
    )



# ==========================================================
# Delete Alert
# ==========================================================


@router.delete(
    "/{alert_id}",
)
async def delete_alert(
    alert_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Delete alert.
    """

    service = AlertService(db)

    await service.delete_alert(alert_id)

    return {
        "success": True,
        "message": "Alert deleted successfully",
    }



# ==========================================================
# Alert Statistics
# ==========================================================


@router.get(
    "/stats/summary",
)
async def alert_statistics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Alert dashboard statistics.
    """

    service = AlertService(db)

    return await service.get_statistics()