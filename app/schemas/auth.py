"""
Authentication Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import (
    EmailStr,
    Field,
    SecretStr,
)

from app.schemas.base import BaseSchema


# ==========================================================
# Login
# ==========================================================

class LoginRequest(BaseSchema):
    email: EmailStr
    password: SecretStr


class LoginResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


TokenResponse = LoginResponse


# ==========================================================
# Refresh Token
# ==========================================================

class RefreshTokenRequest(BaseSchema):
    refresh_token: str


class RefreshTokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


# ==========================================================
# Logout
# ==========================================================

class LogoutRequest(BaseSchema):
    refresh_token: str


# ==========================================================
# Forgot Password
# ==========================================================

class ForgotPasswordRequest(BaseSchema):
    email: EmailStr


# ==========================================================
# Reset Password
# ==========================================================

class ResetPasswordRequest(BaseSchema):
    token: str

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )


# ==========================================================
# Change Password
# ==========================================================

class ChangePasswordRequest(BaseSchema):
    old_password: SecretStr

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )


# ==========================================================
# OTP Verification
# ==========================================================

class VerifyOTPRequest(BaseSchema):
    email: EmailStr
    otp: str = Field(
        min_length=4,
        max_length=8,
    )


# ==========================================================
# JWT Payload
# ==========================================================

class TokenPayload(BaseSchema):
    sub: str
    email: EmailStr
    role: str
    organization_id: Optional[str] = None
    exp: datetime


# ==========================================================
# Current User
# ==========================================================

class CurrentUserResponse(BaseSchema):
    id: str
    organization_id: Optional[str] = None

    full_name: str
    email: EmailStr

    role: str

    is_active: bool
    is_superuser: bool

    last_login: Optional[datetime] = None


# ==========================================================
# Password Reset Response
# ==========================================================

class PasswordResetResponse(BaseSchema):
    success: bool = True
    message: str


# ==========================================================
# Login History
# ==========================================================

class LoginHistoryResponse(BaseSchema):
    ip_address: Optional[str]
    user_agent: Optional[str]
    login_time: datetime
    status: str