
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.infrastructure.database.mongodb import get_database
from app.infrastructure.security.jwt import verify_token, TokenData
from app.application.repositories.super_admin_repository import SuperAdminRepository
from app.application.repositories.organization_admin_repository import OrganizationAdminRepository
from app.application.schemas.auth import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/super-admin/login")


async def get_db() -> AsyncIOMotorDatabase:
    return await get_database()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token)
    if not token_data:
        raise credentials_exception

    if token_data.role == Role.SUPER_ADMIN:
        repo = SuperAdminRepository(db)
        user = await repo.get_by_id(token_data.id)
    elif token_data.role == Role.ORGANIZATION_ADMIN:
        repo = OrganizationAdminRepository(db)
        user = await repo.get_by_id(token_data.id)
    else:
        raise credentials_exception
    
    if not user:
        raise credentials_exception
    
    user["role"] = token_data.role
    return user


async def get_super_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != Role.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    return current_user


async def get_organization_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in [Role.SUPER_ADMIN, Role.ORGANIZATION_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    return current_user
