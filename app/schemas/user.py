"""
User Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    EmailStr,
    Field,
    SecretStr,
)

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class UserBase(BaseSchema):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
    )


# ==========================================================
# Create
# ==========================================================

class UserCreate(UserBase):

    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    organization_id: UUID

    role_id: UUID

    team_id: Optional[UUID] = None


# ==========================================================
# Update
# ==========================================================

class UserUpdate(BaseSchema):

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    phone: Optional[str] = None

    role_id: Optional[UUID] = None

    team_id: Optional[UUID] = None

    is_active: Optional[bool] = None


# ==========================================================
# Change Password
# ==========================================================

class UserPasswordUpdate(BaseSchema):

    old_password: SecretStr

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )


# ==========================================================
# User Response
# ==========================================================

class UserResponse(BaseResponseSchema):

    organization_id: UUID

    role_id: UUID

    team_id: Optional[UUID] = None

    full_name: str

    email: EmailStr

    phone: Optional[str]

    is_verified: bool

    last_login: Optional[datetime]


# ==========================================================
# User Profile
# ==========================================================

class UserProfileResponse(UserResponse):

    role_name: Optional[str] = None

    organization_name: Optional[str] = None

    team_name: Optional[str] = None


# ==========================================================
# User List
# ==========================================================

class UserListResponse(BaseSchema):

    users: list[UserResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# User Filter
# ==========================================================

class UserFilter(BaseSchema):

    search: Optional[str] = None

    organization_id: Optional[UUID] = None

    role_id: Optional[UUID] = None

    team_id: Optional[UUID] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# User Status
# ==========================================================

class UserStatusUpdate(BaseSchema):

    is_active: bool


# ==========================================================
# User Delete
# ==========================================================

class UserDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "User deleted successfully."