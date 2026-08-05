"""
Authentication API

Handles:
- Login
- Refresh Token
- Logout
- Current User
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


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
    """
    Authenticate user and return JWT tokens.
    """

    service = AuthService(db)

    return await service.login(credentials)


# ==========================================================
# Refresh Token
# ==========================================================

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Access Token",
)
async def refresh_token(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a new access token.
    """

    service = AuthService(db)

    return await service.refresh_token(payload.refresh_token)


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
    """
    Logout current user.
    """

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
    """
    Returns authenticated user.
    """

    return current_user