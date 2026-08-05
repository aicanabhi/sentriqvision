"""
Service Repository

Database operations for AI Services.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate

from app.repositories.base_repository import BaseRepository


class ServiceRepository(
    BaseRepository[Service]
):
    """
    Repository for AI Service management.
    """


    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(
            model=Service,
            session=session
        )


    # ======================================================
    # Create Service
    # ======================================================

    async def create_service(
        self,
        data: ServiceCreate
    ) -> Service:

        service = Service(
            **data.model_dump()
        )

        self.session.add(service)

        await self.session.commit()

        await self.session.refresh(service)

        return service



    # ======================================================
    # Get By ID
    # ======================================================

    async def get_by_id(
        self,
        service_id: UUID
    ) -> Optional[Service]:

        query = select(Service).where(
            Service.id == service_id
        )

        result = await self.session.execute(
            query
        )

        return result.scalar_one_or_none()



    # ======================================================
    # Get By Slug
    # ======================================================

    async def get_by_slug(
        self,
        slug: str
    ) -> Optional[Service]:

        query = select(Service).where(
            Service.slug == slug
        )

        result = await self.session.execute(
            query
        )

        return result.scalar_one_or_none()



    # ======================================================
    # List Services
    # ======================================================

    async def get_all(
        self,
        active_only: bool = True
    ) -> List[Service]:

        query = select(Service)


        if active_only:
            query = query.where(
                Service.is_active == True
            )


        result = await self.session.execute(
            query
        )


        return list(
            result.scalars().all()
        )



    # ======================================================
    # Update Service
    # ======================================================

    async def update_service(
        self,
        service_id: UUID,
        data: ServiceUpdate
    ) -> Optional[Service]:


        values = data.model_dump(
            exclude_unset=True
        )


        if not values:
            return await self.get_by_id(
                service_id
            )


        query = (
            update(Service)
            .where(
                Service.id == service_id
            )
            .values(**values)
        )


        await self.session.execute(
            query
        )


        await self.session.commit()


        return await self.get_by_id(
            service_id
        )



    # ======================================================
    # Delete Service
    # ======================================================

    async def delete_service(
        self,
        service_id: UUID
    ) -> bool:


        query = (
            delete(Service)
            .where(
                Service.id == service_id
            )
        )


        result = await self.session.execute(
            query
        )


        await self.session.commit()


        return result.rowcount > 0



    # ======================================================
    # Enable / Disable
    # ======================================================

    async def change_status(
        self,
        service_id: UUID,
        status: bool
    ) -> Optional[Service]:


        query = (
            update(Service)
            .where(
                Service.id == service_id
            )
            .values(
                is_active=status
            )
        )


        await self.session.execute(
            query
        )


        await self.session.commit()


        return await self.get_by_id(
            service_id
        )