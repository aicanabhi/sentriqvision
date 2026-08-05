"""
Notification Repository
Database operations for notifications.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


class NotificationRepository:
    """
    Notification database access layer.
    """

    def __init__(self, db: AsyncSession):
        self.db = db


    # ======================================================
    # Create Notification
    # ======================================================

    async def create(
        self,
        notification_data: dict,
    ) -> Notification:

        notification = Notification(
            **notification_data
        )

        self.db.add(notification)

        await self.db.commit()

        await self.db.refresh(notification)

        return notification


    # ======================================================
    # Get By ID
    # ======================================================

    async def get_by_id(
        self,
        notification_id: UUID,
    ) -> Optional[Notification]:

        result = await self.db.execute(
            select(Notification)
            .where(
                Notification.id == notification_id
            )
        )

        return result.scalar_one_or_none()


    # ======================================================
    # Get User Notifications
    # ======================================================

    async def get_user_notifications(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ):

        result = await self.db.execute(
            select(Notification)
            .where(
                Notification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
            .limit(limit)
            .offset(offset)
        )

        return result.scalars().all()


    # ======================================================
    # Count User Notifications
    # ======================================================

    async def count_user_notifications(
        self,
        user_id: UUID,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(Notification.id)
            )
            .where(
                Notification.user_id == user_id
            )
        )

        return result.scalar_one()


    # ======================================================
    # Count Unread Notifications
    # ======================================================

    async def count_unread(
        self,
        user_id: UUID,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(Notification.id)
            )
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        )

        return result.scalar_one()


    # ======================================================
    # Mark As Read
    # ======================================================

    async def mark_as_read(
        self,
        notification_id: UUID,
    ) -> bool:

        result = await self.db.execute(
            update(Notification)
            .where(
                Notification.id == notification_id
            )
            .values(
                is_read=True
            )
        )

        await self.db.commit()

        return result.rowcount > 0


    # ======================================================
    # Mark All Read For User
    # ======================================================

    async def mark_all_as_read(
        self,
        user_id: UUID,
    ) -> bool:

        result = await self.db.execute(
            update(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .values(
                is_read=True
            )
        )

        await self.db.commit()

        return result.rowcount > 0


    # ======================================================
    # Delete Notification
    # ======================================================

    async def delete(
        self,
        notification_id: UUID,
    ) -> bool:

        result = await self.db.execute(
            delete(Notification)
            .where(
                Notification.id == notification_id
            )
        )

        await self.db.commit()

        return result.rowcount > 0