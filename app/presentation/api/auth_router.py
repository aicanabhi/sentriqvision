
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.schemas.auth import (
    LoginRequest, TokenResponse, ChangePasswordRequest
)
from app.application.schemas.common import APIResponse
from app.application.services.auth_service import AuthService
from app.infrastructure.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/super-admin/login", response_model=APIResponse[TokenResponse])
async def super_admin_login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        service = AuthService()
        token = await service.login_super_admin(request.email, request.password, db)
        return APIResponse(
            success=True,
            message="Login successful",
            data=token
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/super-admin/logout")
async def super_admin_logout(
    token: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = AuthService()
    await service.logout(token, db)
    return APIResponse(success=True, message="Logout successful")


@router.post("/organization/login", response_model=APIResponse[TokenResponse])
async def organization_admin_login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        service = AuthService()
        token = await service.login_organization_admin(request.email, request.password, db)
        return APIResponse(
            success=True,
            message="Login successful",
            data=token
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh-token", response_model=APIResponse[TokenResponse])
async def refresh_token(token: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        service = AuthService()
        new_tokens = await service.refresh_access_token(token, db)
        return APIResponse(
            success=True,
            message="Token refreshed",
            data=new_tokens
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = AuthService()
        await service.change_password(
            current_user["id"],
            current_user["role"],
            request.old_password,
            request.new_password,
            db
        )
        return APIResponse(success=True, message="Password changed successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/profile")
async def get_profile(current_user = Depends(get_current_user)):
    return APIResponse(
        success=True,
        data={
            "id": current_user["id"],
            "email": current_user["email"],
            "name": current_user["name"],
            "role": current_user["role"]
        }
    )
