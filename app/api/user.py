"""
User API

User Management Endpoints
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_active_user,
    get_current_org_admin,
    pagination_params,
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter()


# ==========================================================
# Create User
# ==========================================================

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Create a new user.
    """

    service = UserService(db)

    return await service.create_user(user)


# ==========================================================
# List Users
# ==========================================================

@router.get("")
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    List users.
    """

    service = UserService(db)

    return await service.list_users(
        page=page,
        per_page=per_page,
    )


# ==========================================================
# Get User
# ==========================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get user by ID.
    """

    service = UserService(db)

    return await service.get_user(user_id)


# ==========================================================
# Update User
# ==========================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Update user.
    """

    service = UserService(db)

    return await service.update_user(
        user_id,
        user,
    )


# ==========================================================
# Delete User
# ==========================================================

@router.delete(
    "/{user_id}",
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Delete user.
    """

    service = UserService(db)

    await service.delete_user(user_id)

    return {
        "success": True,
        "message": "User deleted successfully",
    }


# ==========================================================
# Activate User
# ==========================================================

@router.patch(
    "/{user_id}/activate",
)
async def activate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Activate user.
    """

    service = UserService(db)

    return await service.activate_user(user_id)


# ==========================================================
# Deactivate User
# ==========================================================

@router.patch(
    "/{user_id}/deactivate",
)
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Deactivate user.
    """

    service = UserService(db)

    return await service.deactivate_user(user_id)


# ==========================================================
# Reset Password
# ==========================================================

@router.patch(
    "/{user_id}/reset-password",
)
async def reset_password(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Reset user password.
    """

    service = UserService(db)

    return await service.reset_password(user_id)


# ==========================================================
# User Profile
# ==========================================================

@router.get(
    "/me/profile",
)
async def my_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Logged-in user profile.
    """

    service = UserService(db)

    return await service.get_profile(current_user["id"])


# ==========================================================
# Update Profile
# ==========================================================

@router.put(
    "/me/profile",
)
async def update_profile(
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update own profile.
    """

    service = UserService(db)

    return await service.update_profile(
        current_user["id"],
        user,
    )