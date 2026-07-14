
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.schemas.user import UserCreate, UserUpdate, UserResponse
from app.application.schemas.common import APIResponse
from app.application.services.user_service import UserService
from app.infrastructure.utils.dependencies import get_db, get_organization_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=APIResponse[UserResponse])
async def create_user(
    request: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    user = await service.create_user(
        current_user["organization_id"],
        request,
        current_user["id"]
    )
    return APIResponse(success=True, data=user)


@router.get("", response_model=APIResponse[List[UserResponse]])
async def get_all_users(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    users = await service.get_all_users(current_user["organization_id"])
    return APIResponse(success=True, data=users)


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
async def get_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    user = await service.get_user_by_id(user_id, current_user["organization_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=user)


@router.put("/{user_id}", response_model=APIResponse[UserResponse])
async def update_user(
    user_id: str,
    request: UserUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    user = await service.update_user(
        user_id,
        current_user["organization_id"],
        request,
        current_user["id"]
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    success = await service.delete_user(user_id, current_user["organization_id"])
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, message="User deleted")


@router.patch("/{user_id}/activate", response_model=APIResponse[UserResponse])
async def activate_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    user = await service.activate_user(user_id, current_user["organization_id"], current_user["id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=user)


@router.patch("/{user_id}/suspend", response_model=APIResponse[UserResponse])
async def suspend_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    user = await service.suspend_user(user_id, current_user["organization_id"], current_user["id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=user)


@router.patch("/{user_id}/reset-password")
async def reset_user_password(
    user_id: str,
    new_password: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = UserService(db)
    await service.reset_user_password(user_id, current_user["organization_id"], new_password, current_user["id"])
    return APIResponse(success=True, message="Password reset successful")
