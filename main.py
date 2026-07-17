from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.services.auth_service import AuthService
from app.config import settings

# API Routers
from app.presentation.api.auth_router import router as auth_router
from app.presentation.api.dashboard_router import router as dashboard_router
from app.presentation.api.super_admin_router import router as super_admin_router
from app.presentation.api.organization_router import router as organization_router
from app.presentation.api.team_router import router as team_router
from app.presentation.api.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting SentriQVision...")

    try:
        auth_service = AuthService()
        await auth_service.create_super_admin()
        print("✓ Super Admin initialized")
    except Exception as e:
        print(f"Warning: {e}")

    yield

    print("Stopping SentriQVision...")


app = FastAPI(
    title="SentriQVision Enterprise AI Camera Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# ==========================
# Authentication
# ==========================
app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
)

# ==========================
# Dashboard
# ==========================
app.include_router(
    dashboard_router,
    prefix=settings.API_PREFIX,
)

# ==========================
# Super Admin
# ==========================
app.include_router(
    super_admin_router,
    prefix=settings.API_PREFIX,
)

# ==========================
# Organization
# ==========================
app.include_router(
    organization_router,
    prefix=settings.API_PREFIX,
)

# ==========================
# Teams
# ==========================
app.include_router(
    team_router,
    prefix=settings.API_PREFIX,
)

# ==========================
# Users
# ==========================
app.include_router(
    user_router,
    prefix=settings.API_PREFIX,
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "SentriQVision Enterprise AI Camera Intelligence Platform",
        "version": "1.0.0",
        "status": "Running"
    }