import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event_evidence import EventEvidence

class EventEvidenceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            evidence_id: uuid.UUID,
    ) -> EventEvidence | None:
        result = await self.session.execute(select(EventEvidence).where(EventEvidence.id == evidence_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[EventEvidence]:
        result = await self.session.execute(select(EventEvidence).order_by(EventEvidence.captured_at.desc()))
        return list(result.scalars().all())

    async def get_by_event(
            self,
            event_id: uuid.UUID,
    ) -> list[EventEvidence]:
        result = await self.session.execute(select(EventEvidence).where(EventEvidence.id == event_id).order_by(EventEvidence.captured_at.desc()))
        return list(result.scalars().all())

    async def create(
            self,
            event_id: uuid.UUID,
            evidence_type: str,
            storage_key: str,
            mime_type: str,
            captured_at,
    ) -> EventEvidence:
        evidence = EventEvidence(
            event_id=event_id,
            evidence_type=evidence_type,
            storage_key=storage_key,
            mime_type=mime_type,
            captured_at=captured_at,
        )

        self.session.add(evidence)
        await self.session.flush()

        return evidence

    async def delete(
            self,
            evidence: EventEvidence,
    ) -> None:
        await self.session.delete(evidence)