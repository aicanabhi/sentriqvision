"""
User Management Service
"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User


class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================================================
    # Create User
    # ==========================================================

    async def create_user(self, user_data):

        user = User(
            email=user_data.email,
            username=user_data.email.split("@")[0],   # Temporary username
            full_name=user_data.full_name,
            hashed_password=hash_password(
                user_data.password.get_secret_value()
            ),
            organization_id=str(user_data.organization_id),
        )

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ==========================================================
    # Count Users
    # ==========================================================

    async def count_users(self):

        result = await self.db.execute(
            select(func.count(User.id))
        )

        return result.scalar() or 0

    # ==========================================================
    # List Users
    # ==========================================================

    async def list_users(
        self,
        page: int = 1,
        per_page: int = 20,
    ):

        offset = (page - 1) * per_page

        result = await self.db.execute(
            select(User)
            .offset(offset)
            .limit(per_page)
        )

        return result.scalars().all()

    # ==========================================================
    # Get User
    # ==========================================================

    async def get_user(
        self,
        user_id,
    ):

        print("Searching:", user_id)

        result = await self.db.execute(
            select(User).where(User.id == str(user_id))
        )

        user = result.scalar_one_or_none()

        print("Found:", user)

        return user

    # ==========================================================
    # Update User
    # ==========================================================

    async def update_user(
        self,
        user_id,
        user_data,
    ):

        user = await self.get_user(user_id)

        if not user:
            return None

        data = user_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for key, value in data.items():

            if key == "password":

                user.hashed_password = hash_password(
                    value.get_secret_value()
                )

            elif hasattr(user, key):

                setattr(
                    user,
                    key,
                    value,
                )

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ==========================================================
    # Delete User
    # ==========================================================

    async def delete_user(
        self,
        user_id,
    ):

        user = await self.get_user(user_id)

        if not user:
            return False

        await self.db.delete(user)

        await self.db.commit()

        return True

    # ==========================================================
    # Activate User
    # ==========================================================

    async def activate_user(
        self,
        user_id,
    ):

        user = await self.get_user(user_id)

        if not user:
            return None

        user.is_active = True

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ==========================================================
    # Deactivate User
    # ==========================================================

    async def deactivate_user(
        self,
        user_id,
    ):

        user = await self.get_user(user_id)

        if not user:
            return None

        user.is_active = False

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ==========================================================
    # Reset Password
    # ==========================================================

    async def reset_password(
        self,
        user_id,
    ):

        user = await self.get_user(user_id)

        if not user:
            return None

        default_password = "Password@123"

        user.hashed_password = hash_password(
            default_password
        )

        await self.db.commit()
        await self.db.refresh(user)

        return {
            "success": True,
            "message": "Password reset successfully.",
            "new_password": default_password,
        }

    # ==========================================================
    # Get Profile
    # ==========================================================

    async def get_profile(
        self,
        user_id,
    ):

        return await self.get_user(user_id)

    # ==========================================================
    # Update Profile
    # ==========================================================

    async def update_profile(
        self,
        user_id,
        user_data,
    ):

        return await self.update_user(
            user_id,
            user_data,
        )