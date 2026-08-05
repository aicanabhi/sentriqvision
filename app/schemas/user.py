"""
User Schemas
"""

from __future__ import annotations

from uuid import UUID

from pydantic import (
    EmailStr,
    Field,
    SecretStr,
)

from app.schemas.base import (
    BaseSchema,
    BaseResponseSchema,
)


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


# ==========================================================
# Create
# ==========================================================

class UserCreate(UserBase):

    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    organization_id: UUID


# ==========================================================
# Update
# ==========================================================

class UserUpdate(BaseSchema):

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    email: EmailStr | None = None


# ==========================================================
# Response
# ==========================================================

class UserResponse(BaseResponseSchema):

    full_name: str

    email: EmailStr

    organization_id: UUID


# ==========================================================
# List Response
# ==========================================================

class UserListResponse(BaseSchema):

    users: list[UserResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Delete Response
# ==========================================================

class UserDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "User deleted successfully."