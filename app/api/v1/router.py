from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    cameras,
    health,
    users,
    events,
    alerts,
    alert_rules,
    parameters,
    superadmin,
    reports,
    face_access,
    anpr,
    analytics,
    websocket,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["Cameras"])
api_router.include_router(health.router, prefix="/health", tags=["Health & System Metrics"])
api_router.include_router(events.router, prefix="/events", tags=["Events & Detections"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alert Management"])
api_router.include_router(alert_rules.router, prefix="/alert-rules", tags=["Alert Rules"])
api_router.include_router(parameters.router, prefix="/parameters", tags=["54 AI Parameters"])
api_router.include_router(superadmin.router, prefix="/superadmin", tags=["Super Admin Platform Control"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reporting & PDF/CSV Export"])
api_router.include_router(face_access.router, prefix="/face-access", tags=["Face Recognition & Access Control"])
api_router.include_router(anpr.router, prefix="/anpr", tags=["ANPR & Vehicle Analytics"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Tenant Analytics"])
api_router.include_router(websocket.router, tags=["WebSockets"])
