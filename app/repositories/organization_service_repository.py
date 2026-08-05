"""
Organization Service Repository

Handles database operations for
Organization <-> AI Service mapping.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_service import OrganizationService
from app.schemas.organization_service import (
    OrganizationServiceCreate,
    OrganizationServiceUpdate,
)


class OrganizationServiceRepository:
    """
    Repository for organization services.
    """


    # ======================================================
    # Create / Enable Service
    # ======================================================

    async def create(
        self,
        db: AsyncSession,
        data: OrganizationServiceCreate,
    ) -> OrganizationService:

        service = OrganizationService(
            **data.model_dump()
        )

        db.add(service)

        await db.commit()

        await db.refresh(service)

        return service



    # ======================================================
    # Get By ID
    # ======================================================

    async def get_by_id(
        self,
        db: AsyncSession,
        service_id: UUID,
    ) -> Optional[OrganizationService]:

        result = await db.execute(
            select(OrganizationService)
            .where(
                OrganizationService.id == service_id
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # Get Organization Services
    # ======================================================

    async def get_by_organization(
        self,
        db: AsyncSession,
        organization_id: UUID,
        enabled_only: bool = False,
    ) -> List[OrganizationService]:

        query = select(
            OrganizationService
        ).where(
            OrganizationService.organization_id
            == organization_id
        )


        if enabled_only:
            query = query.where(
                OrganizationService.is_enabled == True
            )


        result = await db.execute(query)

        return result.scalars().all()



    # ======================================================
    # Get Specific Service
    # ======================================================

    async def get_service(
        self,
        db: AsyncSession,
        organization_id: UUID,
        service_id: UUID,
    ) -> Optional[OrganizationService]:


        result = await db.execute(
            select(OrganizationService)
            .where(
                OrganizationService.organization_id
                == organization_id
            )
            .where(
                OrganizationService.service_id
                == service_id
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # Update Configuration
    # ======================================================

    async def update(
        self,
        db: AsyncSession,
        service: OrganizationService,
        data: OrganizationServiceUpdate,
    ) -> OrganizationService:


        update_data = data.model_dump(
            exclude_unset=True
        )


        for key, value in update_data.items():

            setattr(
                service,
                key,
                value
            )


        await db.commit()

        await db.refresh(service)

        return service



    # ======================================================
    # Enable Service
    # ======================================================

    async def enable(
        self,
        db: AsyncSession,
        organization_id: UUID,
        service_id: UUID,
    ):


        service = await self.get_service(
            db,
            organization_id,
            service_id,
        )


        if service:

            service.is_enabled = True

            await db.commit()

            await db.refresh(service)


        return service



    # ======================================================
    # Disable Service
    # ======================================================

    async def disable(
        self,
        db: AsyncSession,
        organization_id: UUID,
        service_id: UUID,
    ):


        service = await self.get_service(
            db,
            organization_id,
            service_id,
        )


        if service:

            service.is_enabled = False

            await db.commit()

            await db.refresh(service)


        return service



    # ======================================================
    # Delete
    # ======================================================

    async def delete(
        self,
        db: AsyncSession,
        service_id: UUID,
    ) -> bool:


        result = await db.execute(
            delete(OrganizationService)
            .where(
                OrganizationService.id
                == service_id
            )
        )


        await db.commit()


        return result.rowcount > 0



    # ======================================================
    # Check Service Enabled
    # ======================================================

    async def is_enabled(
        self,
        db: AsyncSession,
        organization_id: UUID,
        service_id: UUID,
    ) -> bool:


        result = await db.execute(
            select(
                OrganizationService.id
            )
            .where(
                OrganizationService.organization_id
                == organization_id
            )
            .where(
                OrganizationService.service_id
                == service_id
            )
            .where(
                OrganizationService.is_enabled
                == True
            )
        )


        return result.scalar_one_or_none() is not None