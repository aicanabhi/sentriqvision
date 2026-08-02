"""
Alert Repository

Database operations for AI alerts.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.repositories.base_repository import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    """
    Repository for Alert model.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(
            db=db,
            model=Alert
        )


    # ======================================================
    # Get Alert
    # ======================================================

    async def get_by_id(
        self,
        alert_id: UUID
    ) -> Optional[Alert]:

        query = select(Alert).where(
            Alert.id == alert_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()



    # ======================================================
    # Get Organization Alerts
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[Alert]:

        query = (
            select(Alert)
            .where(
                Alert.organization_id == organization_id
            )
            .order_by(
                Alert.created_at.desc()
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())



    # ======================================================
    # Camera Alerts
    # ======================================================

    async def get_by_camera(
        self,
        camera_id: UUID,
        limit: int = 50
    ) -> List[Alert]:

        query = (
            select(Alert)
            .where(
                Alert.camera_id == camera_id
            )
            .order_by(
                Alert.created_at.desc()
            )
            .limit(limit)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())



    # ======================================================
    # Filter Alerts
    # ======================================================

    async def filter_alerts(
        self,
        organization_id: Optional[UUID] = None,
        camera_id: Optional[UUID] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Alert]:


        query = select(Alert)


        if organization_id:
            query = query.where(
                Alert.organization_id == organization_id
            )


        if camera_id:
            query = query.where(
                Alert.camera_id == camera_id
            )


        if severity:
            query = query.where(
                Alert.severity == severity
            )


        if status:
            query = query.where(
                Alert.status == status
            )


        query = (
            query
            .order_by(
                Alert.created_at.desc()
            )
            .limit(limit)
            .offset(offset)
        )


        result = await self.db.execute(query)

        return list(result.scalars().all())



    # ======================================================
    # Update Status
    # ======================================================

    async def update_status(
        self,
        alert_id: UUID,
        status: str
    ) -> Optional[Alert]:


        query = (
            update(Alert)
            .where(
                Alert.id == alert_id
            )
            .values(
                status=status
            )
            .returning(Alert)
        )


        result = await self.db.execute(query)

        await self.db.commit()


        return result.scalar_one_or_none()



    # ======================================================
    # Assign Alert
    # ======================================================

    async def assign_alert(
        self,
        alert_id: UUID,
        user_id: UUID
    ) -> Optional[Alert]:


        query = (
            update(Alert)
            .where(
                Alert.id == alert_id
            )
            .values(
                assigned_to=user_id
            )
            .returning(Alert)
        )


        result = await self.db.execute(query)

        await self.db.commit()


        return result.scalar_one_or_none()



    # ======================================================
    # Count Alerts
    # ======================================================

    async def count_alerts(
        self,
        organization_id: UUID
    ) -> int:


        query = (
            select(
                func.count(Alert.id)
            )
            .where(
                Alert.organization_id == organization_id
            )
        )


        result = await self.db.execute(query)

        return result.scalar() or 0



    # ======================================================
    # Delete Alert
    # ======================================================

    async def delete_alert(
        self,
        alert_id: UUID
    ) -> bool:


        query = (
            delete(Alert)
            .where(
                Alert.id == alert_id
            )
        )


        result = await self.db.execute(query)

        await self.db.commit()


        return result.rowcount > 0