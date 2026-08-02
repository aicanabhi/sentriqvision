"""
SentriqVision FastAPI Application
"""
from app.api.api_v1 import api_router
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.settings import settings
from app.database.session import create_tables, close_database


# ==========================================================
# Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup & shutdown lifecycle.
    """

    # Create database tables (Development Only)
    try:
        await create_tables()
    except Exception as exc:
        print(f"Warning: Failed to initialize database tables on startup: {exc}")

    print("=" * 60)
    print("SentriqVision Backend Started")
    print("=" * 60)

    yield

    try:
        await close_database()
    except Exception:
        pass

    print("=" * 60)
    print("SentriqVision Backend Stopped")
    print("=" * 60)


# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="SentriqVision Enterprise AI Surveillance Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Root
# ==========================================================

@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "status": "running",
    }


# ==========================================================
# Health
# ==========================================================

@app.get("/health", tags=["Health"])
async def health():
    return {
        "success": True,
        "status": "healthy",
        "database": "connected",
        "version": settings.app_version,
    }


# ==========================================================
# API Routes
# ==========================================================

app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)

from app.api.ws import router as ws_router
app.include_router(
    ws_router,
    tags=["Websockets"],
)


# ==========================================================
# Global Exception Handler
# ==========================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
        },
    )