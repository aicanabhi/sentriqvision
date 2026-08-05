"""
API Version 1 Router

Collects all application routers.
"""

from fastapi import APIRouter

from app.api.alert import router as alert_router
from app.api.auth import router as auth_router
from app.api.camera import router as camera_router
from app.api.dashboard import router as dashboard_router
from app.api.detection import router as detection_router
from app.api.nortification import router as notification_router
from app.api.organization import router as organization_router
from app.api.permission import router as permission_router
from app.api.report import router as report_router
from app.api.role import router as role_router
from app.api.service import router as service_router
from app.api.super_admin import router as super_admin_router
from app.api.user import router as user_router

# ==========================================================
# Main API Router
# ==========================================================

api_router = APIRouter()

# ==========================================================
# Dashboard
# ==========================================================

api_router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)

# ==========================================================
# Organization
# ==========================================================

api_router.include_router(
    organization_router,
    prefix="/organizations",
    tags=["Organizations"],
)

# ==========================================================
# Users
# ==========================================================

api_router.include_router(
    user_router,
    prefix="/users",
    tags=["Users"],
)

# ==========================================================
# Roles
# ==========================================================

api_router.include_router(
    role_router,
    prefix="/roles",
    tags=["Roles"],
)

# ==========================================================
# Permissions
# ==========================================================

api_router.include_router(
    permission_router,
    prefix="/permissions",
    tags=["Permissions"],
)

# ==========================================================
# Services
# ==========================================================

api_router.include_router(
    service_router,
    prefix="/services",
    tags=["Services"],
)

# ==========================================================
# Cameras
# ==========================================================

api_router.include_router(
    camera_router,
    prefix="/cameras",
    tags=["Cameras"],
)

# ==========================================================
# Detection
# ==========================================================

api_router.include_router(
    detection_router,
    prefix="/detections",
    tags=["Detections"],
)

# ==========================================================
# Alerts
# ==========================================================

api_router.include_router(
    alert_router,
    prefix="/alerts",
    tags=["Alerts"],
)

# ==========================================================
# Reports
# ==========================================================

api_router.include_router(
    report_router,
    prefix="/reports",
    tags=["Reports"],
)

# ==========================================================
# Super Admin
# ==========================================================

api_router.include_router(
    super_admin_router,
    prefix="/super-admin",
    tags=["Super Admin"],
)

# ==========================================================
# Authentication
# ==========================================================

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

# ==========================================================
# Notifications
# ==========================================================

api_router.include_router(
    notification_router,
    prefix="/notifications",
    tags=["Notifications"],
)