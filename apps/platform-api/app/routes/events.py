import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.schemas.event import EventCreate, EventResponse
from app.services.event import EventService
from app.models.camera import Camera
from app.models.site import Site
from app.repositories.access import AccessRepository
from app.security.dependencies import get_current_account
from app.services.access import AccessService

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Get events
@router.get("/", response_model=list[EventResponse])
async def list_events(session: AsyncSession = Depends(get_db)):
    service = EventService(session)
    return await service.get_all()

# Get events by camera
@router.get("/camera/{camera_id}", response_model=list[EventResponse])
async def list_events_by_camera(camera_id: uuid.UUID, account=Depends(get_current_account), session: AsyncSession = Depends(get_db)):

    camera = await session.get(Camera, camera_id)

    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")

    site = await session.get(Site, camera.site_id)

    if site is None:
        raise HTTPException(status_code=404, detail="Camera Site not found")

    repository = AccessRepository(session)
    access_service = AccessService(repository)

    allowed = await access_service.has_camera_access(
        account=account,
        camera_id=camera.id,
        camera_site_id=camera.site_id,
        camera_site_organization_id=site.organization_id,
    )

    if not allowed:
        raise HTTPException(status_code=403, detail="You do not have access to this camera")

    service = EventService(session)

    return await service.get_by_camera(camera_id)

# Get events by zone
@router.get("/zone/{zone_id}", response_model=list[EventResponse])
async def list_events_by_zone(zone_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = EventService(session)
    return await service.get_by_zone(zone_id)

# Get event by module
@router.get("/module/{module_id}", response_model=list[EventResponse])
async def list_events_by_module(module_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = EventService(session)
    return await service.get_by_module(module_id)

# Get event by event type
@router.get("/type/{event_type}", response_model=list[EventResponse])
async def list_events_by_type(event_type: str, session: AsyncSession = Depends(get_db)):
    service = EventService(session)
    return await service.get_by_event_type(event_type)

# Get event by ID
@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = EventService(session)
    event = await service.get_by_id(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Create events
@router.post("/", response_model=EventResponse)
async def create_event(event: EventCreate, session: AsyncSession = Depends(get_db)):
    service = EventService(session)

    try:
        event = await service.create(
            camera_id=event.camera_id,
            zone_id=event.zone_id,
            module_id=event.module_id,
            event_type=event.event_type,
            condition_id=event.condition_id,
            occurred_at=event.occurred_at,
            event_metadata=event.event_metadata,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    await session.commit()
    await session.refresh(event)
    return event

# Delete event
@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    service = EventService(session)
    event = await service.get_by_id(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    await service.delete(event_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)