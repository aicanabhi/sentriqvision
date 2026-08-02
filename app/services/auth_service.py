"""
Authentication Service
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse


class AuthService:
    """
    Service handling user authentication logic.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, credentials: LoginRequest) -> TokenResponse:
        """
        Authenticate user with email and password.
        """
        password_str = credentials.password.get_secret_value()

        result = await self.db.execute(
            select(User).where(User.email == str(credentials.email))
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(password_str, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        subject = str(user.id)
        access_token = create_access_token(
            subject=subject,
            extra_data={"email": user.email, "role": "super_admin" if user.is_super_admin else "user"},
        )
        refresh_token = create_refresh_token(subject=subject)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=900,
        )

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """
        Generate a new access token from refresh token.
        """
        try:
            payload = verify_token(refresh_token, expected_type="refresh")
            user_id = payload.get("sub")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        result = await self.db.execute(
            select(User).where(User.id == int(user_id) if str(user_id).isdigit() else User.id)
        )
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        new_access = create_access_token(
            subject=str(user.id),
            extra_data={"email": user.email, "role": "super_admin" if user.is_super_admin else "user"},
        )
        new_refresh = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="Bearer",
            expires_in=900,
        )

    async def logout(self, current_user) -> None:
        """
        Perform logout cleanup.
        """
        return None
