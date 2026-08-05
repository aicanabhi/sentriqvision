"""
Organization Repository

Database operations for Organization model.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(
    BaseRepository[Organization]
):

    def __init__(
        self,
        db: AsyncSession
    ):
        super().__init__(
            db,
            Organization
        )


    # ======================================================
    # Get Organization By Code
    # ======================================================

    async def get_by_code(
        self,
        code: str
    ) -> Optional[Organization]:

        result = await self.db.execute(
            select(Organization)
            .where(
                Organization.code == code
            )
        )

        return result.scalar_one_or_none()


    # ======================================================
    # Get Organization By Email
    # ======================================================

    async def get_by_email(
        self,
        email: str
    ) -> Optional[Organization]:

        result = await self.db.execute(
            select(Organization)
            .where(
                Organization.email == email
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # List Organizations
    # ======================================================

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20
    ) -> List[Organization]:

        result = await self.db.execute(
            select(Organization)
            .offset(skip)
            .limit(limit)
            .order_by(
                Organization.created_at.desc()
            )
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Search Organizations
    # ======================================================

    async def search(
        self,
        keyword: str
    ) -> List[Organization]:

        result = await self.db.execute(
            select(Organization)
            .where(
                Organization.name.ilike(
                    f"%{keyword}%"
                )
            )
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Count Organizations
    # ======================================================

    async def count(
        self
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(
                    Organization.id
                )
            )
        )

        return result.scalar_one()



    # ======================================================
    # Activate Organization
    # ======================================================

    async def activate(
        self,
        organization_id: UUID
    ):

        await self.db.execute(
            update(Organization)
            .where(
                Organization.id == organization_id
            )
            .values(
                is_active=True
            )
        )

        await self.db.commit()



    # ======================================================
    # Deactivate Organization
    # ======================================================

    async def deactivate(
        self,
        organization_id: UUID
    ):

        await self.db.execute(
            update(Organization)
            .where(
                Organization.id == organization_id
            )
            .values(
                is_active=False
            )
        )

        await self.db.commit()



    # ======================================================
    # Delete Organization
    # ======================================================

    async def delete_by_id(
        self,
        organization_id: UUID
    ):

        await self.db.execute(
            delete(Organization)
            .where(
                Organization.id == organization_id
            )
        )

        await self.db.commit()