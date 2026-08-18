import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.event import Event

class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, event_id: uuid.UUID) -> Event | None:
        result = await self.session.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Event]:
        result = await self.session.execute(select(Event).order_by(Event.occurred_at.desc()))
        return list(result.scalars().all())

    async def get_by_camera(self, camera_id: uuid.UUID) -> list[Event]:
        result = await self.session.execute(select(Event).where(Event.camera_id == camera_id).order_by(Event.occurred_at.desc()))
        return list(result.scalars().all())

    async def get_by_zone(self, zone_id: uuid.UUID) -> list[Event]:
        result = await self.session.execute(select(Event).where(Event.zone_id == zone_id).order_by(Event.occurred_at.desc()))
        return list(result.scalars().all())

    async def get_by_module(self, module_id: uuid.UUID) -> list[Event]:
        result = await self.session.execute(select(Event).where(Event.module_id == module_id).order_by(Event.occurred_at.desc()))
        return list(result.scalars().all())

    async def get_by_event_type(self, event_type: uuid.UUID) -> list[Event]:
        result = await self.session.execute(select(Event).where(Event.event_type == event_type).order_by(Event.occurred_at.desc()))
        return list(result.scalars().all())

    async def create(
            self,
            camera_id: uuid.UUID,
            zone_id: uuid.UUID,
            module_id: uuid.UUID,
            event_type: str,
            condition_id: float,
            occurred_at: datetime,
            event_metadata: dict
    ) -> Event:
        event = Event(
            camera_id = camera_id,
            zone_id = zone_id,
            module_id = module_id,
            event_type = event_type,
            condition_id=condition_id,
            occurred_at = occurred_at,
            event_metadata = event_metadata
        )

        self.session.add(event)
        await self.session.flush()

        return event

    async def delete(
            self,
            event: Event,
    ) -> None:
        await self.session.delete(event)