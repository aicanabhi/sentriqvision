"""
Dashboard API

Provides system overview and analytics.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_active_user,
)

from app.services.dashboard_service import DashboardService


router = APIRouter()


# ==========================================================
# Dashboard Overview
# ==========================================================

@router.get(
    "/overview",
    tags=["Dashboard"],
)
async def dashboard_overview(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Returns complete dashboard overview.
    """

    service = DashboardService(db)

    return await service.get_overview(
        current_user=current_user
    )


# ==========================================================
# Organization Statistics
# ==========================================================

@router.get(
    "/organizations",
    tags=["Dashboard"],
)
async def organization_statistics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Organization statistics.
    """

    service = DashboardService(db)

    return await service.organization_stats()


# ==========================================================
# Camera Statistics
# ==========================================================

@router.get(
    "/cameras",
    tags=["Dashboard"],
)
async def camera_statistics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Camera monitoring statistics.
    """

    service = DashboardService(db)

    return await service.camera_stats()


# ==========================================================
# Alert Statistics
# ==========================================================

@router.get(
    "/alerts",
    tags=["Dashboard"],
)
async def alert_statistics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Alert analytics.
    """

    service = DashboardService(db)

    return await service.alert_stats()


# ==========================================================
# AI Detection Statistics
# ==========================================================

@router.get(
    "/detections",
    tags=["Dashboard"],
)
async def detection_statistics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    AI detection analytics.
    """

    service = DashboardService(db)

    return await service.detection_stats()


# ==========================================================
# System Health
# ==========================================================

@router.get(
    "/health",
    tags=["Dashboard"],
)
async def system_health(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Backend and service health.
    """

    service = DashboardService(db)

    return await service.system_health()