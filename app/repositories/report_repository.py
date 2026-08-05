"""
Report Repository
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import Report
from app.repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository[Report]):
    """
    Repository for report database operations.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            model=Report,
            session=session,
        )


    # ======================================================
    # Get Reports
    # ======================================================

    async def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Report]:

        query = (
            select(Report)
            .where(
                Report.organization_id == organization_id
            )
            .order_by(
                desc(Report.created_at)
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())


    # ======================================================
    # Count Reports
    # ======================================================

    async def count_by_organization(
        self,
        organization_id: UUID,
    ) -> int:

        query = (
            select(func.count())
            .select_from(Report)
            .where(
                Report.organization_id == organization_id
            )
        )

        result = await self.session.execute(query)

        return result.scalar_one()


    # ======================================================
    # Find By Type
    # ======================================================

    async def get_by_type(
        self,
        organization_id: UUID,
        report_type: str,
    ) -> list[Report]:

        query = (
            select(Report)
            .where(
                Report.organization_id == organization_id,
                Report.report_type == report_type,
            )
            .order_by(
                desc(Report.created_at)
            )
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())


    # ======================================================
    # Find Generated Reports
    # ======================================================

    async def get_completed_reports(
        self,
        organization_id: UUID,
    ) -> list[Report]:

        query = (
            select(Report)
            .where(
                Report.organization_id == organization_id,
                Report.status == "completed",
            )
            .order_by(
                desc(Report.created_at)
            )
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())


    # ======================================================
    # Search Reports
    # ======================================================

    async def search(
        self,
        organization_id: UUID,
        keyword: str,
    ) -> list[Report]:

        query = (
            select(Report)
            .where(
                Report.organization_id == organization_id,
                Report.name.ilike(
                    f"%{keyword}%"
                ),
            )
            .order_by(
                desc(Report.created_at)
            )
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())


    # ======================================================
    # Update Status
    # ======================================================

    async def update_status(
        self,
        report_id: UUID,
        status: str,
    ) -> Optional[Report]:

        report = await self.get(report_id)

        if not report:
            return None


        report.status = status

        await self.session.commit()

        await self.session.refresh(report)

        return report


    # ======================================================
    # Delete Report
    # ======================================================

    async def delete_report(
        self,
        report_id: UUID,
    ) -> bool:

        report = await self.get(report_id)

        if not report:
            return False


        await self.session.delete(report)

        await self.session.commit()

        return True