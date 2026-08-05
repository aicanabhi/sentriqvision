"""
Authentication API

Handles:
- Login
- Logout
- Current User
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_active_user,
    get_db,
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

from app.schemas.user import UserResponse
from app.services.auth_service import AuthService


router = APIRouter(
    tags=["Authentication"]
)


# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User Login",
)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.login(credentials)


# ==========================================================
# Logout
# ==========================================================

@router.post(
    "/logout",
    summary="Logout User",
)
async def logout(
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    await service.logout(current_user)

    return {
        "success": True,
        "message": "Logged out successfully",
    }


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current User",
)
async def get_me(
    current_user=Depends(get_current_active_user),
):
    return current_user