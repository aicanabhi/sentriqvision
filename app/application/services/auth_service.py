
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import settings
from app.application.repositories.super_admin_repository import SuperAdminRepository
from app.application.repositories.organization_admin_repository import OrganizationAdminRepository
from app.application.repositories.refresh_token_repository import RefreshTokenRepository
from app.infrastructure.security.hash import get_password_hash, verify_password
from app.infrastructure.security.jwt import create_access_token, create_refresh_token, verify_token
from app.application.schemas.auth import Role, TokenResponse
from datetime import datetime


class AuthService:
    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self.db = db

    async def create_super_admin(self):
        try:
            if not self.db:
                from app.infrastructure.database.mongodb import get_database
                self.db = await get_database()
                
            repo = SuperAdminRepository(self.db)
            existing = await repo.get_by_email(settings.SUPER_ADMIN_EMAIL)
            if not existing:
                hashed_password = get_password_hash(settings.SUPER_ADMIN_PASSWORD)
                await repo.create({
                    "email": settings.SUPER_ADMIN_EMAIL,
                    "password": hashed_password,
                    "name": "Super Admin"
                })
                print("Super Admin created successfully!")
            else:
                print("Super Admin already exists!")
        except Exception as e:
            print(f"Database connection failed (MongoDB not running?): {e}")

    async def login_super_admin(self, email: str, password: str, db: AsyncIOMotorDatabase):
        repo = SuperAdminRepository(db)
        user = await repo.get_by_email(email)
        if not user or not verify_password(password, user["password"]):
            raise ValueError("Invalid credentials")
        
        access_token = create_access_token(
            data={"sub": user["id"], "role": Role.SUPER_ADMIN}
        )
        refresh_token = create_refresh_token(
            data={"sub": user["id"], "role": Role.SUPER_ADMIN}
        )
        
        refresh_repo = RefreshTokenRepository(db)
        await refresh_repo.create({
            "token": refresh_token,
            "user_id": user["id"],
            "role": Role.SUPER_ADMIN,
            "revoked": False
        })
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def login_organization_admin(self, email: str, password: str, db: AsyncIOMotorDatabase):
        repo = OrganizationAdminRepository(db)
        user = await repo.get_by_email(email)
        if not user or not verify_password(password, user["password"]):
            raise ValueError("Invalid credentials")
        
        access_token = create_access_token(
            data={"sub": user["id"], "role": Role.ORGANIZATION_ADMIN, "organization_id": user["organization_id"]}
        )
        refresh_token = create_refresh_token(
            data={"sub": user["id"], "role": Role.ORGANIZATION_ADMIN, "organization_id": user["organization_id"]}
        )
        
        refresh_repo = RefreshTokenRepository(db)
        await refresh_repo.create({
            "token": refresh_token,
            "user_id": user["id"],
            "role": Role.ORGANIZATION_ADMIN,
            "revoked": False
        })
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def logout(self, refresh_token: str, db: AsyncIOMotorDatabase):
        refresh_repo = RefreshTokenRepository(db)
        token_doc = await refresh_repo.get_by_field("token", refresh_token)
        if token_doc:
            await refresh_repo.update(token_doc["id"], {"revoked": True})

    async def refresh_access_token(self, refresh_token: str, db: AsyncIOMotorDatabase):
        refresh_repo = RefreshTokenRepository(db)
        token_doc = await refresh_repo.get_by_field("token", refresh_token)
        
        if not token_doc or token_doc["revoked"]:
            raise ValueError("Invalid refresh token")
        
        token_data = verify_token(refresh_token)
        if not token_data:
            raise ValueError("Invalid refresh token")
        
        new_access_token = create_access_token(
            data={"sub": token_data.id, "role": token_data.role}
        )
        new_refresh_token = create_refresh_token(
            data={"sub": token_data.id, "role": token_data.role}
        )
        
        await refresh_repo.update(token_doc["id"], {"revoked": True})
        await refresh_repo.create({
            "token": new_refresh_token,
            "user_id": token_data.id,
            "role": token_data.role,
            "revoked": False
        })
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    async def change_password(self, user_id: str, role: str, old_password: str, new_password: str, db: AsyncIOMotorDatabase):
        if role == Role.SUPER_ADMIN:
            repo = SuperAdminRepository(db)
        else:
            repo = OrganizationAdminRepository(db)
        
        user = await repo.get_by_id(user_id)
        if not user or not verify_password(old_password, user["password"]):
            raise ValueError("Invalid old password")
        
        hashed_password = get_password_hash(new_password)
        await repo.update(user_id, {"password": hashed_password})
