"""
API Version 1 Router

Collects all application routers.
"""

from fastapi import APIRouter
from app.api.camera_group import router as camera_group_router

from app.api.auth import router as auth_router
from app.api.super_admin import router as super_admin_router

from app.api.organization import router as organization_router
from app.api.user import router as user_router
from app.api.role import router as role_router
from app.api.permission import router as permission_router

from app.api.camera import router as camera_router
from app.api.detection import router as detection_router
from app.api.alert import router as alert_router
from app.api.notification import router as notification_router

from app.api.dashboard import router as dashboard_router
from app.api.report import router as report_router

from app.api.service import router as service_router


# ==========================================================
# Main API Router
# ==========================================================

api_router = APIRouter()


# ==========================================================
# 1. Authentication
# ==========================================================

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# 2. Super Admin
# ==========================================================

api_router.include_router(
    super_admin_router,
    prefix="/super-admin",
    tags=["Super Admin"],
)


# ==========================================================
# 3. Organization Management
# ==========================================================

api_router.include_router(
    organization_router,
    prefix="/organizations",
    tags=["Organizations"],
)


# ==========================================================
# 4. User Management
# ==========================================================

api_router.include_router(
    user_router,
    prefix="/users",
    tags=["Users"],
)


# ==========================================================
# 5. Role Management
# ==========================================================

api_router.include_router(
    role_router,
    prefix="/roles",
    tags=["Roles"],
)


# ==========================================================
# 6. Permission Management
# ==========================================================

api_router.include_router(
    permission_router,
    prefix="/permissions",
    tags=["Permissions"],
)


# ==========================================================
# 7. Camera Management (Core Feature)
# ==========================================================

api_router.include_router(
    camera_router,
    prefix="/cameras",
    tags=["Cameras"],
)

api_router.include_router(
    camera_group_router
)


# ==========================================================
# 8. AI Detection
# ==========================================================

api_router.include_router(
    detection_router,
    prefix="/detections",
    tags=["Detections"],
)


# ==========================================================
# 9. Alerts
# ==========================================================

api_router.include_router(
    alert_router,
    prefix="/alerts",
    tags=["Alerts"],
)


# ==========================================================
# 10. Notifications
# ==========================================================

api_router.include_router(
    notification_router,
    prefix="/notifications",
    tags=["Notifications"],
)


# ==========================================================
# 11. Dashboard
# ==========================================================

api_router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ==========================================================
# 12. Reports
# ==========================================================

api_router.include_router(
    report_router,
    prefix="/reports",
    tags=["Reports"],
)


# ==========================================================
# 13. Services
# ==========================================================

api_router.include_router(
    service_router,
    prefix="/services",
    tags=["Services"],
)