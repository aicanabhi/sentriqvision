"""
Camera Health Repository

Handles database operations for camera health monitoring.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_health import CameraHealth
from app.repositories.base_repository import BaseRepository


class CameraHealthRepository(
    BaseRepository[CameraHealth]
):
    """
    Repository for camera health records.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db=db,
            model=CameraHealth,
        )


    # ======================================================
    # Get Latest Health Status
    # ======================================================

    async def get_latest_health(
        self,
        camera_id: UUID,
    ) -> Optional[CameraHealth]:

        query = (
            select(CameraHealth)
            .where(
                CameraHealth.camera_id == camera_id
            )
            .order_by(
                desc(CameraHealth.created_at)
            )
            .limit(1)
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()


    # ======================================================
    # Camera Health History
    # ======================================================

    async def get_health_history(
        self,
        camera_id: UUID,
        limit: int = 50,
    ):

        query = (
            select(CameraHealth)
            .where(
                CameraHealth.camera_id == camera_id
            )
            .order_by(
                desc(CameraHealth.created_at)
            )
            .limit(limit)
        )

        result = await self.db.execute(query)

        return result.scalars().all()


    # ======================================================
    # Update Heartbeat
    # ======================================================

    async def update_heartbeat(
        self,
        camera_id: UUID,
    ):

        health = await self.get_latest_health(
            camera_id
        )

        if health:

            health.last_seen = datetime.utcnow()

            health.status = "ONLINE"

            await self.db.commit()

            await self.db.refresh(
                health
            )

        return health


    # ======================================================
    # Get Offline Cameras
    # ======================================================

    async def get_offline_cameras(
        self,
        timeout_minutes: int = 5,
    ):

        from datetime import timedelta


        threshold = (
            datetime.utcnow()
            -
            timedelta(
                minutes=timeout_minutes
            )
        )


        query = (
            select(CameraHealth)
            .where(
                CameraHealth.last_seen < threshold
            )
        )


        result = await self.db.execute(
            query
        )

        return result.scalars().all()


    # ======================================================
    # Create Health Record
    # ======================================================

    async def create_health_record(
        self,
        camera_id: UUID,
        status: str,
        cpu_usage: float = 0,
        memory_usage: float = 0,
        fps: float = 0,
        latency: float = 0,
    ):

        health = CameraHealth(
            camera_id=camera_id,
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            fps=fps,
            latency=latency,
            last_seen=datetime.utcnow(),
        )


        self.db.add(
            health
        )

        await self.db.commit()

        await self.db.refresh(
            health
        )

        return health