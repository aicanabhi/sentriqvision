# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from motor.motor_asyncio import AsyncIOMotorDatabase

# from app.application.schemas.auth import (
#     TokenResponse,
#     ChangePasswordRequest,
# )
# from app.application.schemas.common import APIResponse
# from app.application.services.auth_service import AuthService
# from app.infrastructure.utils.dependencies import get_db, get_current_user

# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"]
# )


# @router.post("/login", response_model=APIResponse[TokenResponse])
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     try:
#         service = AuthService()

#         token = await service.login_super_admin(
#             form_data.username,   # Email
#             form_data.password,
#             db
#         )

#         return APIResponse(
#             success=True,
#             message="Login successful",
#             data=token
#         )

#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=str(e)
#         )


# @router.post("/logout")
# async def logout(
#     token: str,
#     db: AsyncIOMotorDatabase = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     service = AuthService()

#     await service.logout(
#         token,
#         db
#     )

#     return APIResponse(
#         success=True,
#         message="Logout successful"
#     )


# @router.post("/refresh-token", response_model=APIResponse[TokenResponse])
# async def refresh_token(
#     token: str,
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     try:
#         service = AuthService()

#         new_tokens = await service.refresh_access_token(
#             token,
#             db
#         )

#         return APIResponse(
#             success=True,
#             message="Token refreshed",
#             data=new_tokens
#         )

#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=str(e)
#         )


# @router.post("/change-password")
# async def change_password(
#     request: ChangePasswordRequest,
#     db: AsyncIOMotorDatabase = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     try:
#         service = AuthService()

#         await service.change_password(
#             current_user["id"],
#             current_user["role"],
#             request.old_password,
#             request.new_password,
#             db
#         )

#         return APIResponse(
#             success=True,
#             message="Password changed successfully"
#         )

#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )


# @router.get("/profile")
# async def get_profile(
#     current_user=Depends(get_current_user)
# ):
#     return APIResponse(
#         success=True,
#         data={
#             "id": current_user["id"],
#             "email": current_user["email"],
#             "name": current_user["name"],
#             "role": current_user["role"]
#         }
#     )

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.application.services.auth_service import AuthService
from app.application.schemas.auth import (
    TokenResponse,
    ChangePasswordRequest
)

from app.application.schemas.common import APIResponse
from app.infrastructure.utils.dependencies import (
    get_db,
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



# ==========================
# Login
# ==========================
@router.post(
    "/login",
    response_model=APIResponse[TokenResponse]
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db)
):

    try:

        service = AuthService()


        token = await service.login_super_admin(
            form_data.username,
            form_data.password,
            db
        )


        return APIResponse(
            success=True,
            message="Login successful",
            data=token
        )


    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )



# ==========================
# Logout
# ==========================
@router.post("/logout")
async def logout(
    current_user=Depends(get_current_user)
):

    return APIResponse(
        success=True,
        message="Logout successful"
    )



# ==========================
# Change Password
# ==========================
@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user=Depends(get_current_user)
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


        return APIResponse(
            success=True,
            message="Password changed successfully"
        )


    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )