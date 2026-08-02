"""
Camera Stream Repository

Database operations for camera streams.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_stream import CameraStream
from app.repositories.base_repository import BaseRepository


class CameraStreamRepository(
    BaseRepository[CameraStream]
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            CameraStream
        )


    # ======================================================
    # Get stream by ID
    # ======================================================

    async def get_by_id(
        self,
        stream_id: UUID,
    ) -> Optional[CameraStream]:

        result = await self.session.execute(
            select(CameraStream)
            .where(
                CameraStream.id == stream_id
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # Get streams by camera
    # ======================================================

    async def get_by_camera(
        self,
        camera_id: UUID,
    ) -> list[CameraStream]:

        result = await self.session.execute(
            select(CameraStream)
            .where(
                CameraStream.camera_id == camera_id
            )
            .order_by(
                CameraStream.created_at.desc()
            )
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Get active streams
    # ======================================================

    async def get_active_streams(
        self,
    ) -> list[CameraStream]:

        result = await self.session.execute(
            select(CameraStream)
            .where(
                CameraStream.is_active == True
            )
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # Create stream
    # ======================================================

    async def create_stream(
        self,
        stream_data: dict,
    ) -> CameraStream:

        stream = CameraStream(
            **stream_data
        )

        self.session.add(stream)

        await self.session.commit()

        await self.session.refresh(
            stream
        )

        return stream



    # ======================================================
    # Update stream
    # ======================================================

    async def update_stream(
        self,
        stream_id: UUID,
        data: dict,
    ) -> Optional[CameraStream]:

        await self.session.execute(
            update(CameraStream)
            .where(
                CameraStream.id == stream_id
            )
            .values(
                **data
            )
        )

        await self.session.commit()

        return await self.get_by_id(
            stream_id
        )



    # ======================================================
    # Update stream status
    # ======================================================

    async def update_status(
        self,
        stream_id: UUID,
        status: str,
    ) -> Optional[CameraStream]:

        return await self.update_stream(
            stream_id,
            {
                "status": status
            }
        )



    # ======================================================
    # Update last frame time
    # ======================================================

    async def update_last_frame(
        self,
        stream_id: UUID,
    ):

        from datetime import datetime, timezone

        return await self.update_stream(
            stream_id,
            {
                "last_frame_at":
                datetime.now(timezone.utc)
            }
        )



    # ======================================================
    # Delete stream
    # ======================================================

    async def delete_stream(
        self,
        stream_id: UUID,
    ) -> bool:

        result = await self.session.execute(
            delete(CameraStream)
            .where(
                CameraStream.id == stream_id
            )
        )

        await self.session.commit()

        return result.rowcount > 0