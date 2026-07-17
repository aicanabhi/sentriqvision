from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.infrastructure.database.mongodb import get_database
from app.infrastructure.security.jwt import verify_token

from app.application.repositories.super_admin_repository import (
    SuperAdminRepository
)

from app.application.repositories.organization_admin_repository import (
    OrganizationAdminRepository
)

from app.application.schemas.auth import Role


security = HTTPBearer()


async def get_db() -> AsyncIOMotorDatabase:
    return await get_database()



async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_db)
):

    token = credentials.credentials

    print("=" * 50)
    print("TOKEN RECEIVED:", token)


    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )


    token_data = verify_token(token)


    print("TOKEN DATA:", token_data)



    if not token_data:
        raise credentials_exception



    user_id = token_data.id
    role = token_data.role



    if role == Role.SUPER_ADMIN.value:

        repo = SuperAdminRepository(db)

        user = await repo.get_by_id(user_id)


    elif role == Role.ORGANIZATION_ADMIN:

        repo = OrganizationAdminRepository(db)

        user = await repo.get_by_id(user_id)


    else:

        raise credentials_exception



    print("USER:", user)



    if not user:
        raise credentials_exception



    user["role"] = role


    return user



# ==================================
# SUPER ADMIN CHECK
# ==================================

async def get_super_admin(
    current_user = Depends(get_current_user)
):

    if current_user.get("role") != Role.SUPER_ADMIN:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access required"
        )


    return current_user


# ==================================
# ORGANIZATION ADMIN CHECK
# ==================================

async def get_organization_admin(
    current_user = Depends(get_current_user)
):

    if current_user.get("role") != Role.ORGANIZATION_ADMIN.value:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization Admin access required"
        )


    return current_user