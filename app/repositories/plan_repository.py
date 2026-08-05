"""
Plan Repository
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan
from app.repositories.base_repository import BaseRepository


class PlanRepository(BaseRepository[Plan]):
    """
    Repository for Plan operations.
    """

    def __init__(self):
        super().__init__(Plan)

    # =====================================================
    # Get by ID
    # =====================================================

    async def get_by_id(
        self,
        db: AsyncSession,
        plan_id: UUID,
    ) -> Optional[Plan]:

        result = await db.execute(
            select(Plan).where(Plan.id == plan_id)
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get by Code
    # =====================================================

    async def get_by_code(
        self,
        db: AsyncSession,
        code: str,
    ) -> Optional[Plan]:

        result = await db.execute(
            select(Plan).where(
                Plan.code == code
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get by Name
    # =====================================================

    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
    ) -> Optional[Plan]:

        result = await db.execute(
            select(Plan).where(
                Plan.name == name
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # List Active Plans
    # =====================================================

    async def get_active(
        self,
        db: AsyncSession,
    ) -> list[Plan]:

        result = await db.execute(
            select(Plan)
            .where(Plan.is_active == True)
            .order_by(Plan.name)
        )

        return result.scalars().all()

    # =====================================================
    # Public Plans
    # =====================================================

    async def get_public(
        self,
        db: AsyncSession,
    ) -> list[Plan]:

        result = await db.execute(
            select(Plan)
            .where(
                Plan.is_public == True,
                Plan.is_active == True,
            )
            .order_by(Plan.price)
        )

        return result.scalars().all()

    # =====================================================
    # Default Plan
    # =====================================================

    async def get_default(
        self,
        db: AsyncSession,
    ) -> Optional[Plan]:

        result = await db.execute(
            select(Plan).where(
                Plan.is_default == True
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Search
    # =====================================================

    async def search(
        self,
        db: AsyncSession,
        keyword: str,
    ) -> list[Plan]:

        result = await db.execute(
            select(Plan).where(
                Plan.name.ilike(f"%{keyword}%")
            )
        )

        return result.scalars().all()

    # =====================================================
    # Exists
    # =====================================================

    async def exists(
        self,
        db: AsyncSession,
        code: str,
    ) -> bool:

        result = await db.execute(
            select(Plan).where(
                Plan.code == code
            )
        )

        return result.scalar_one_or_none() is not None


plan_repository = PlanRepository()