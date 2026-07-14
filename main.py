from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.application.services.auth_service import AuthService
from app.presentation.api.auth_router import router as auth_router
from app.presentation.api.super_admin_router import router as super_admin_router
from app.presentation.api.organization_router import router as organization_router
from app.presentation.api.team_router import router as team_router
from app.presentation.api.user_router import router as user_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    try:
        auth_service = AuthService()
        await auth_service.create_super_admin()
        print("Super admin check complete")
    except Exception as e:
        print(f"Warning: Could not initialize super admin (MongoDB not running?): {e}")
    yield


app = FastAPI(
    title="SentriQVision Enterprise AI Camera Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(super_admin_router, prefix=settings.API_PREFIX)
app.include_router(organization_router, prefix=settings.API_PREFIX)
app.include_router(team_router, prefix=settings.API_PREFIX)
app.include_router(user_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {"message": "SentriQVision API Running"}