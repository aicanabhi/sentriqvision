import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event_evidence import EventEvidence
from app.repositories.event_evidence import EventEvidenceRepository

class EventEvidenceService:
    def __init__(self, session: AsyncSession):
        self.repository = EventEvidenceRepository(session)

    async def get_by_id(
            self,
            evidence_id: uuid.UUID,
    ) -> EventEvidence | None:
        return await self.repository.get_by_id(evidence_id)

    async def get_all(self) -> list[EventEvidence]:
        return await self.repository.get_all()

    async def get_by_event(
            self,
            event_id: uuid.UUID,
    ) -> list[EventEvidence]:
        return await self.repository.get_by_event(event_id)

    async def create(
            self,
            event_id: uuid.UUID,
            evidence_type: str,
            storage_key: str,
            mime_type: str,
            captured_at: datetime,
    ) -> EventEvidence:

        evidence_type = evidence_type.strip().upper()
        storage_key = storage_key.strip()
        mime_type = mime_type.strip()

        if not evidence_type:
            raise ValueError("Evidence type cannot be empty")

        if evidence_type not in {"SNAPSHOT", "VIDEO"}:
            raise ValueError("Evidence type must be either SNAPSHOT or VIDEO")

        if not storage_key:
            raise ValueError("Storage key cannot be empty")

        if not mime_type:
            raise ValueError("Mime type cannot be empty")

        return await self.repository.create(
            event_id=event_id,
            evidence_type=evidence_type,
            storage_key=storage_key,
            mime_type=mime_type,
            captured_at=captured_at,
        )

    async def delete(
            self,
            evidence_id: uuid.UUID,
    ) -> None:
        evidence = await self.repository.get_by_id(evidence_id)

        if evidence is None:
            raise ValueError("Evidence does not exist")

        await self.repository.delete(evidence)