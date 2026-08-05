"""
Audit Repository

Database operations for audit logs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import Audit
from app.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[Audit]):
    """
    Repository for Audit Logs.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            Audit
        )


    # ======================================================
    # Create Audit Log
    # ======================================================

    async def create_log(
        self,
        *,
        user_id: Optional[UUID] = None,
        organization_id: Optional[UUID] = None,
        action: str,
        module: str,
        description: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Audit:
        """
        Create new audit entry.
        """

        audit = Audit(
            user_id=user_id,
            organization_id=organization_id,
            action=action,
            module=module,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.session.add(audit)

        await self.session.flush()

        return audit



    # ======================================================
    # Get By ID
    # ======================================================

    async def get_by_id(
        self,
        audit_id: UUID,
    ) -> Optional[Audit]:

        query = select(Audit).where(
            Audit.id == audit_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()



    # ======================================================
    # Organization Audit History
    # ======================================================

    async def get_organization_logs(
        self,
        organization_id: UUID,
        limit: int = 100,
    ) -> list[Audit]:

        query = (
            select(Audit)
            .where(
                Audit.organization_id == organization_id
            )
            .order_by(
                desc(Audit.created_at)
            )
            .limit(limit)
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())



    # ======================================================
    # User Activity History
    # ======================================================

    async def get_user_logs(
        self,
        user_id: UUID,
        limit: int = 100,
    ) -> list[Audit]:

        query = (
            select(Audit)
            .where(
                Audit.user_id == user_id
            )
            .order_by(
                desc(Audit.created_at)
            )
            .limit(limit)
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())



    # ======================================================
    # Filter Logs
    # ======================================================

    async def filter_logs(
        self,
        *,
        organization_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> list[Audit]:


        query = select(Audit)


        if organization_id:
            query = query.where(
                Audit.organization_id == organization_id
            )


        if user_id:
            query = query.where(
                Audit.user_id == user_id
            )


        if module:
            query = query.where(
                Audit.module == module
            )


        if action:
            query = query.where(
                Audit.action == action
            )


        if start_date:
            query = query.where(
                Audit.created_at >= start_date
            )


        if end_date:
            query = query.where(
                Audit.created_at <= end_date
            )


        query = (
            query
            .order_by(
                desc(Audit.created_at)
            )
            .limit(limit)
        )


        result = await self.session.execute(query)

        return list(result.scalars().all())



    # ======================================================
    # Count Logs
    # ======================================================

    async def count_logs(
        self,
        organization_id: Optional[UUID] = None,
    ) -> int:

        query = select(
            func.count(Audit.id)
        )


        if organization_id:
            query = query.where(
                Audit.organization_id == organization_id
            )


        result = await self.session.execute(query)

        return result.scalar_one()