"""
User API

User Management Endpoints
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_active_user,
    get_current_org_admin,
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
    service = UserService(db)

    user = await service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


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
    service = UserService(db)

    user = await service.update_user(
        user_id,
        user,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# ==========================================================
# Delete User
# ==========================================================

@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    service = UserService(db)

    success = await service.delete_user(user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "success": True,
        "message": "User deleted successfully",
    }


# ==========================================================
# Activate User
# ==========================================================

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
)
async def activate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    service = UserService(db)

    user = await service.activate_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# ==========================================================
# Deactivate User
# ==========================================================

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
)
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    service = UserService(db)

    user = await service.deactivate_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


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
    service = UserService(db)

    result = await service.reset_password(user_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return result


# ==========================================================
# My Profile
# ==========================================================

@router.get(
    "/me/profile",
    response_model=UserResponse,
)
async def my_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = UserService(db)

    user = await service.get_profile(current_user["id"])

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# ==========================================================
# Update My Profile
# ==========================================================

@router.put(
    "/me/profile",
    response_model=UserResponse,
)
async def update_profile(
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = UserService(db)

    updated_user = await service.update_profile(
        current_user["id"],
        user,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return updated_user