import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.schemas.event_evidence import EventEvidenceCreate, EventEvidenceResponse
from app.services.event_evidence import EventEvidenceService
from app.models.event import Event
from app.models.camera import Camera
from app.models.site import Site
from app.repositories.access import AccessRepository
from app.security.dependencies import get_current_account
from app.services.access import AccessService

router = APIRouter(
    prefix="/event_evidence",
    tags=["event-evidence"],
)

async def get_db() -> AsyncSession:
   async with AsyncSessionLocal() as session:
       yield session

# Get all evidence
@router.get("/", response_model=list[EventEvidenceResponse])
async def list_evidence(session: AsyncSession = Depends(get_db)):
    service = EventEvidenceService(session)
    return await service.get_all()

# Get evidence by event
@router.get("/event/{event_id}", response_model=list[EventEvidenceResponse])
async def list_evidence_by_event(
        event_id: uuid.UUID,
        account=Depends(get_current_account),
        session: AsyncSession = Depends(get_db),
):
    event = await session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    camera = await session.get(Camera, event.camera_id)

    if camera is None:
        raise HTTPException(status_code=404, detail="Camera site not found")

    repository = AccessRepository(session)
    access_service = AccessService(repository)

    allowed = await access_service.has_camera_access(
        account=account,
        camera_id=camera.id,
        camera_site_id=camera.site_id,
        camera_site_organization_id=Site.organization_id,
    )

    if not allowed:
        raise HTTPException(status_code=403, detail="Access denied")

    service = EventEvidenceService(session)
    return await service.get_by_event(event_id)

# Get specific evidence by ID
@router.get("/{evidence_id}", response_model=EventEvidenceResponse)
async def get_evidence(evidence_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = EventEvidenceService(session)
    evidence = await service.get_by_id(evidence_id)

    if evidence is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found")
    return evidence

# Create evidence
@router.post("/", response_model=EventEvidenceResponse)
async def create_evidence(
        data: EventEvidenceCreate,
        session: AsyncSession = Depends(get_db),
):
    service = EventEvidenceService(session)

    try:
        evidence = await service.create(
            event_id=data.event_id,
            evidence_type=data.evidence_type,
            storage_key=data.storage_key,
            mime_type=data.mime_type,
            captured_at=data.captured_at,
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    await session.commit()
    await session.refresh(evidence)

    return evidence

# Delete evidence
@router.delete("/{evidence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_evidence(
        evidence_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = EventEvidenceService(session)

    evidence = await service.get_by_id(evidence_id)

    if evidence is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found")

    await service.delete(evidence_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)