import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event
from app.repositories.event import EventRepository

class EventService:
    def __init__(self, session: AsyncSession):
        self.repository = EventRepository(session)

    async def get_by_id(self, event_id: uuid.UUID) -> Event | None:
        return await self.repository.get_by_id(event_id)

    async def get_all(self) -> list[Event]:
        return await self.repository.get_all()

    async def get_by_camera(self, camera_id: uuid.UUID) -> list[Event]:
        return await self.repository.get_by_camera(camera_id)

    async def get_by_zone(self, zone_id: uuid.UUID) -> list[Event]:
        return await self.repository.get_by_zone(zone_id)

    async def get_by_module(self, module_id: uuid.UUID) -> list[Event]:
        return await self.repository.get_by_module(module_id)

    async def get_by_event_type(self, event_type: str) -> list[Event]:
        return await self.repository.get_by_event_type(event_type)

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
        event_type = event_type.strip().upper()

        if not event_type:
            raise ValueError("Event type cannot be empty")

        if condition_id < 0:
            raise ValueError("Condition ID cannot be negative")

        if not isinstance(event_metadata, dict):
            raise ValueError("Event metadata must be a JSON object")

        return await self.repository.create(
            camera_id=camera_id,
            zone_id=zone_id,
            module_id=module_id,
            event_type=event_type,
            condition_id=condition_id,
            occurred_at=occurred_at,
            event_metadata=event_metadata
        )

    async def delete(self, event_id: uuid.UUID) -> None:
        event = await self.repository.get_by_id(event_id)

        if event is None:
            raise ValueError("Event does not exist")

        await self.repository.delete(event)