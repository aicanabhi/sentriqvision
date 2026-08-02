"""
Service Management Service
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service


class ServiceService:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_service(self, service_data):

        service = Service(
            **service_data.model_dump()
        )

        self.db.add(service)

        await self.db.commit()
        await self.db.refresh(service)

        return service


    async def list_services(self):

        result = await self.db.execute(
            select(Service)
            .where(Service.is_deleted == False)
        )

        return result.scalars().all()


    async def get_service(self, service_id: UUID):

        result = await self.db.execute(
            select(Service)
            .where(
                Service.id == service_id,
                Service.is_deleted == False,
            )
        )

        return result.scalar_one_or_none()


    async def update_service(
        self,
        service_id: UUID,
        service_data,
    ):

        service = await self.get_service(service_id)

        if not service:
            return None


        update_data = service_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                service,
                field,
                value,
            )


        await self.db.commit()
        await self.db.refresh(service)

        return service


    async def delete_service(
        self,
        service_id: UUID,
    ):

        service = await self.get_service(service_id)

        if not service:
            return False


        service.is_deleted = True

        await self.db.commit()

        return True


    async def enable_service(
        self,
        service_id: UUID,
        organization_id: UUID,
    ):

        return {
            "service_id": str(service_id),
            "organization_id": str(organization_id),
            "enabled": True,
        }


    async def disable_service(
        self,
        service_id: UUID,
        organization_id: UUID,
    ):

        return {
            "service_id": str(service_id),
            "organization_id": str(organization_id),
            "enabled": False,
        }