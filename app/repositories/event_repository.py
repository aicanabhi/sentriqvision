"""
Event Repository

Database operations for Event model.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event


class EventRepository:
    """
    Repository for Event database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db


    # ======================================================
    # Create
    # ======================================================

    async def create(
        self,
        event: Event,
    ) -> Event:

        self.db.add(event)

        await self.db.commit()

        await self.db.refresh(event)

        return event


    # ======================================================
    # Get By ID
    # ======================================================

    async def get_by_id(
        self,
        event_id: UUID,
    ) -> Optional[Event]:

        result = await self.db.execute(
            select(Event)
            .where(
                Event.id == event_id
            )
        )

        return result.scalar_one_or_none()


    # ======================================================
    # Organization Events
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ):

        result = await self.db.execute(

            select(Event)
            .where(
                Event.organization_id == organization_id
            )
            .order_by(
                Event.created_at.desc()
            )
            .limit(limit)
            .offset(offset)

        )

        return result.scalars().all()



    # ======================================================
    # Camera Events
    # ======================================================

    async def get_by_camera(
        self,
        camera_id: UUID,
        limit: int = 50,
    ):

        result = await self.db.execute(

            select(Event)
            .where(
                Event.camera_id == camera_id
            )
            .order_by(
                Event.created_at.desc()
            )
            .limit(limit)

        )

        return result.scalars().all()



    # ======================================================
    # Filter Events
    # ======================================================

    async def filter(
        self,
        organization_id: Optional[UUID] = None,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ):


        query = select(Event)


        if organization_id:

            query = query.where(
                Event.organization_id == organization_id
            )


        if event_type:

            query = query.where(
                Event.event_type == event_type
            )


        if severity:

            query = query.where(
                Event.severity == severity
            )


        if status:

            query = query.where(
                Event.status == status
            )


        query = (
            query
            .order_by(
                Event.created_at.desc()
            )
            .limit(limit)
            .offset(offset)
        )


        result = await self.db.execute(query)


        return result.scalars().all()



    # ======================================================
    # Update Status
    # ======================================================

    async def update_status(
        self,
        event_id: UUID,
        status: str,
    ):


        await self.db.execute(

            update(Event)
            .where(
                Event.id == event_id
            )
            .values(
                status=status
            )

        )


        await self.db.commit()


        return await self.get_by_id(event_id)



    # ======================================================
    # Count
    # ======================================================

    async def count(
        self,
        organization_id: UUID,
    ):

        result = await self.db.execute(

            select(
                func.count(Event.id)
            )
            .where(
                Event.organization_id == organization_id
            )

        )


        return result.scalar()



    # ======================================================
    # Delete
    # ======================================================

    async def delete(
        self,
        event_id: UUID,
    ):

        await self.db.execute(

            delete(Event)
            .where(
                Event.id == event_id
            )

        )


        await self.db.commit()

        return True