"""
User Management Service
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_user(self, user_data):

        user = User(
            **user_data.model_dump()
        )

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user


    async def list_users(self):

        result = await self.db.execute(
            select(User)
        )

        return result.scalars().all()


    async def get_user(self, user_id):

        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
        )

        return result.scalar_one_or_none()


    async def update_user(
        self,
        user_id,
        user_data,
    ):

        user = await self.get_user(user_id)

        if not user:
            return None


        for key, value in user_data.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                user,
                key,
                value,
            )


        await self.db.commit()
        await self.db.refresh(user)

        return user


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