
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.repositories.user_repository import UserRepository
from app.application.schemas.user import UserCreate, UserUpdate, UserResponse, UserStatus
from app.infrastructure.security.hash import get_password_hash


class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = UserRepository(db)

    async def create_user(self, organization_id: str, data: UserCreate, created_by: str) -> UserResponse:
        hashed_password = get_password_hash(data.password)
        user_id = await self.repo.create({
            "email": data.email,
            "name": data.name,
            "phone": data.phone,
            "status": data.status,
            "password": hashed_password,
            "organization_id": organization_id,
            "team_id": data.team_id,
            "created_by": created_by,
            "updated_by": created_by
        })
        user = await self.repo.get_by_id(user_id)
        return UserResponse(**user)

    async def get_all_users(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = await self.repo.get_all(
            filter_query={"organization_id": organization_id},
            skip=skip,
            limit=limit
        )
        return [UserResponse(**user) for user in users]

    async def get_user_by_id(self, user_id: str, organization_id: str) -> Optional[UserResponse]:
        user = await self.repo.get_by_id(user_id)
        if user and user["organization_id"] == organization_id:
            return UserResponse(**user)
        return None

    async def update_user(self, user_id: str, organization_id: str, data: UserUpdate, updated_by: str) -> Optional[UserResponse]:
        user = await self.repo.get_by_id(user_id)
        if not user or user["organization_id"] != organization_id:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = updated_by
        updated_user = await self.repo.update(user_id, update_data)
        return UserResponse(**updated_user)

    async def delete_user(self, user_id: str, organization_id: str) -> bool:
        user = await self.repo.get_by_id(user_id)
        if not user or user["organization_id"] != organization_id:
            return False
        return await self.repo.delete(user_id)

    async def activate_user(self, user_id: str, organization_id: str, updated_by: str) -> Optional[UserResponse]:
        user = await self.repo.get_by_id(user_id)
        if not user or user["organization_id"] != organization_id:
            return None
        
        updated_user = await self.repo.update(user_id, {
            "status": UserStatus.ACTIVE,
            "updated_by": updated_by
        })
        return UserResponse(**updated_user)

    async def suspend_user(self, user_id: str, organization_id: str, updated_by: str) -> Optional[UserResponse]:
        user = await self.repo.get_by_id(user_id)
        if not user or user["organization_id"] != organization_id:
            return None
        
        updated_user = await self.repo.update(user_id, {
            "status": UserStatus.SUSPENDED,
            "updated_by": updated_by
        })
        return UserResponse(**updated_user)

    async def reset_user_password(self, user_id: str, organization_id: str, new_password: str, updated_by: str):
        user = await self.repo.get_by_id(user_id)
        if not user or user["organization_id"] != organization_id:
            return None
        
        hashed_password = get_password_hash(new_password)
        await self.repo.update(user_id, {
            "password": hashed_password,
            "updated_by": updated_by
        })
