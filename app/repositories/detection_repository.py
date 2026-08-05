"""
Detection Repository

Database operations for AI detections.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.detection import Detection
from app.repositories.base_repository import BaseRepository


class DetectionRepository(
    BaseRepository[Detection]
):
    """
    Repository for AI detection operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            model=Detection,
            db=db,
        )


    # ======================================================
    # Get By Camera
    # ======================================================

    async def get_by_camera(
        self,
        camera_id: UUID,
        limit: int = 100,
    ):

        query = (
            select(Detection)
            .where(
                Detection.camera_id == camera_id
            )
            .order_by(
                desc(
                    Detection.created_at
                )
            )
            .limit(limit)
        )

        result = await self.db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Get By Organization
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        limit: int = 100,
    ):

        query = (
            select(Detection)
            .where(
                Detection.organization_id
                == organization_id
            )
            .order_by(
                desc(
                    Detection.created_at
                )
            )
            .limit(limit)
        )

        result = await self.db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Detection Type Filter
    # ======================================================

    async def get_by_type(
        self,
        detection_type: str,
        organization_id: Optional[UUID] = None,
    ):

        query = select(
            Detection
        ).where(
            Detection.type == detection_type
        )


        if organization_id:

            query = query.where(
                Detection.organization_id
                == organization_id
            )


        query = query.order_by(
            desc(
                Detection.created_at
            )
        )


        result = await self.db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Date Range Search
    # ======================================================

    async def get_between_dates(
        self,
        start_date: datetime,
        end_date: datetime,
        camera_id: Optional[UUID] = None,
    ):

        query = (
            select(Detection)
            .where(
                Detection.created_at >= start_date,
                Detection.created_at <= end_date,
            )
        )


        if camera_id:

            query = query.where(
                Detection.camera_id == camera_id
            )


        query = query.order_by(
            desc(
                Detection.created_at
            )
        )


        result = await self.db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Count Detections
    # ======================================================

    async def count_by_type(
        self,
        organization_id: UUID,
        detection_type: str,
    ):

        query = select(
            func.count(Detection.id)
        ).where(
            Detection.organization_id
            == organization_id,
            Detection.type
            == detection_type,
        )


        result = await self.db.execute(query)

        return result.scalar()



    # ======================================================
    # Latest Detections
    # ======================================================

    async def latest(
        self,
        organization_id: UUID,
        limit: int = 50,
    ):

        query = (
            select(Detection)
            .where(
                Detection.organization_id
                == organization_id
            )
            .order_by(
                desc(
                    Detection.created_at
                )
            )
            .limit(limit)
        )


        result = await self.db.execute(query)

        return result.scalars().all()