"""
Notification Service
"""

from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


class NotificationService:
    """
    Service handling Notification business logic.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, notification_data: NotificationCreate) -> Notification:
        notification = Notification(**notification_data.model_dump())
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def get_user_notifications(
        self,
        user_id: int | str,
        page: int = 1,
        per_page: int = 20,
    ) -> List[Notification]:
        skip = (page - 1) * per_page
        result = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == str(user_id))
            .offset(skip)
            .limit(per_page)
        )
        return list(result.scalars().all())

    async def get_notification(self, notification_id: UUID | str) -> Notification:
        result = await self.db.execute(
            select(Notification).where(Notification.id == str(notification_id))
        )
        notification = result.scalar_one_or_none()
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        return notification

    async def mark_as_read(self, notification_id: UUID | str) -> Notification:
        notification = await self.get_notification(notification_id)
        notification.is_read = True
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def mark_all_as_read(self, user_id: int | str) -> dict:
        await self.db.execute(
            update(Notification)
            .where(Notification.user_id == str(user_id))
            .values(is_read=True)
        )
        await self.db.commit()
        return {"success": True, "message": "All notifications marked as read"}

    async def update_notification(
        self, notification_id: UUID | str, data: NotificationUpdate
    ) -> Notification:
        notification = await self.get_notification(notification_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(notification, key, value)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def delete_notification(self, notification_id: UUID | str) -> None:
        notification = await self.get_notification(notification_id)
        await self.db.delete(notification)
        await self.db.commit()
