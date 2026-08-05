"""
User Repository

Database operations related to User model.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """
    User database repository.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db


    # ======================================================
    # Create User
    # ======================================================

    async def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user


    # ======================================================
    # Get By ID
    # ======================================================

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> Optional[User]:

        result = await self.db.execute(
            select(User)
            .where(
                User.id == user_id,
                User.is_deleted == False
            )
        )

        return result.scalar_one_or_none()


    # ======================================================
    # Get By Email
    # ======================================================

    async def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:

        result = await self.db.execute(
            select(User)
            .where(
                User.email == email,
                User.is_deleted == False
            )
        )

        return result.scalar_one_or_none()


    # ======================================================
    # Get Organization Users
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:

        result = await self.db.execute(
            select(User)
            .where(
                User.organization_id == organization_id,
                User.is_deleted == False
            )
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())


    # ======================================================
    # Count Organization Users
    # ======================================================

    async def count_by_organization(
        self,
        organization_id: UUID,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(User.id)
            )
            .where(
                User.organization_id == organization_id,
                User.is_deleted == False
            )
        )

        return result.scalar_one()


    # ======================================================
    # Update User
    # ======================================================

    async def update(
        self,
        user_id: UUID,
        values: dict,
    ) -> Optional[User]:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(**values)
        )

        await self.db.commit()

        return await self.get_by_id(user_id)


    # ======================================================
    # Activate / Deactivate User
    # ======================================================

    async def update_status(
        self,
        user_id: UUID,
        status: bool,
    ) -> Optional[User]:

        return await self.update(
            user_id,
            {
                "is_active": status
            }
        )


    # ======================================================
    # Soft Delete
    # ======================================================

    async def delete(
        self,
        user_id: UUID,
    ) -> bool:

        result = await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                is_deleted=True
            )
        )

        await self.db.commit()

        return result.rowcount > 0


    # ======================================================
    # Exists
    # ======================================================

    async def exists_by_email(
        self,
        email: str,
    ) -> bool:

        result = await self.db.execute(
            select(
                User.id
            )
            .where(
                User.email == email
            )
        )

        return result.scalar_one_or_none() is not None