"""
Camera Group Repository

Database operations for Camera Groups.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_group import CameraGroup
from app.repositories.base_repository import BaseRepository


class CameraGroupRepository(
    BaseRepository[CameraGroup]
):
    """
    Camera Group database repository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            model=CameraGroup,
            session=session,
        )


    # ======================================================
    # Get By Organization
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ):

        query = (
            select(CameraGroup)
            .where(
                CameraGroup.organization_id
                == organization_id
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(query)

        return result.scalars().all()


    # ======================================================
    # Get Active Groups
    # ======================================================

    async def get_active_groups(
        self,
        organization_id: UUID,
    ):

        query = (
            select(CameraGroup)
            .where(
                CameraGroup.organization_id
                == organization_id,
                CameraGroup.is_active.is_(True),
            )
        )

        result = await self.session.execute(query)

        return result.scalars().all()


    # ======================================================
    # Search
    # ======================================================

    async def search(
        self,
        organization_id: UUID,
        keyword: str,
    ):

        query = (
            select(CameraGroup)
            .where(
                CameraGroup.organization_id
                == organization_id,
                CameraGroup.name.ilike(
                    f"%{keyword}%"
                ),
            )
        )

        result = await self.session.execute(query)

        return result.scalars().all()


    # ======================================================
    # Count
    # ======================================================

    async def count_by_organization(
        self,
        organization_id: UUID,
    ):

        query = (
            select(func.count())
            .select_from(CameraGroup)
            .where(
                CameraGroup.organization_id
                == organization_id
            )
        )

        result = await self.session.execute(query)

        return result.scalar_one()


    # ======================================================
    # Assign Camera
    # ======================================================

    async def add_camera(
        self,
        group_id: UUID,
        camera_id: UUID,
    ):
        """
        Add camera into group.
        """

        group = await self.get(group_id)

        if group:
            group.cameras.append(camera_id)

            await self.session.commit()

        return group


    # ======================================================
    # Update Status
    # ======================================================

    async def update_status(
        self,
        group_id: UUID,
        status: bool,
    ):

        query = (
            update(CameraGroup)
            .where(
                CameraGroup.id == group_id
            )
            .values(
                is_active=status
            )
        )

        await self.session.execute(query)

        await self.session.commit()

        return True


    # ======================================================
    # Delete Group
    # ======================================================

    async def delete_group(
        self,
        group_id: UUID,
    ):

        query = (
            delete(CameraGroup)
            .where(
                CameraGroup.id == group_id
            )
        )

        await self.session.execute(query)

        await self.session.commit()

        return True