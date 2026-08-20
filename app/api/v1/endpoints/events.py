import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.event import Event, EventFrame
from app.models.camera import Camera
from app.models.user import User
from app.schemas.response import ResponseEnvelope
from app.services.rbac_service import get_current_user

router = APIRouter()


class EventResponse(BaseModel):
    id: str
    camera_id: Optional[str] = None
    camera_name: str = "Unknown Camera"
    event_type: str
    severity: str
    confidence: float
    payload: Dict[str, Any] = {}
    timestamp: str
    snapshot_url: Optional[str] = None


@router.get("/", response_model=ResponseEnvelope[List[EventResponse]])
async def list_events(
    event_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    camera_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists observed system events from PostgreSQL database."""
    query = select(Event).options(selectinload(Event.frames)).where(Event.tenant_id == current_user.tenant_id)

    if event_type:
        query = query.where(Event.event_type.ilike(f"%{event_type}%"))
    if severity:
        query = query.where(Event.severity.ilike(f"%{severity}%"))
    if camera_id:
        try:
            cid = uuid.UUID(camera_id)
            query = query.where(Event.camera_id == cid)
        except ValueError:
            pass

    query = query.order_by(Event.timestamp.desc()).limit(limit)
    res = await db.execute(query)
    events = res.scalars().all()

    # If DB has no events, seed 3 initial events
    if not events:
        cam_query = select(Camera).where(Camera.tenant_id == current_user.tenant_id)
        cam = (await db.execute(cam_query)).scalars().first()
        cid = cam.id if cam else None

        seed_events = [
            Event(
                tenant_id=current_user.tenant_id,
                camera_id=cid,
                event_type="FACE_RECOGNIZED",
                severity="INFO",
                confidence=0.985,
                payload={"person_name": "John Doe", "role": "Executive", "match_score": 0.985},
            ),
            Event(
                tenant_id=current_user.tenant_id,
                camera_id=cid,
                event_type="INTRUSION_DETECTED",
                severity="CRITICAL",
                confidence=0.962,
                payload={"zone": "Server Vault ROI-1", "dwell_sec": 30},
            ),
            Event(
                tenant_id=current_user.tenant_id,
                camera_id=cid,
                event_type="PPE_VIOLATION",
                severity="MEDIUM",
                confidence=0.910,
                payload={"missing_gear": ["helmet", "vest"]},
            ),
        ]
        db.add_all(seed_events)
        await db.commit()

        # Re-query
        res = await db.execute(query)
        events = res.scalars().all()

    # Fetch camera name map
    cam_res = await db.execute(select(Camera).where(Camera.tenant_id == current_user.tenant_id))
    cams = {c.id: c.name for c in cam_res.scalars().all()}

    output = []
    for e in events:
        cname = cams.get(e.camera_id, "Main Perimeter Gate") if e.camera_id else "Main Perimeter Gate"
        frame_url = e.frames[0].storage_path if e.frames else "/snapshots/default-event.jpg"
        output.append(
            EventResponse(
                id=str(e.id),
                camera_id=str(e.camera_id) if e.camera_id else None,
                camera_name=cname,
                event_type=e.event_type,
                severity=e.severity,
                confidence=e.confidence,
                payload=e.payload or {},
                timestamp=e.timestamp.isoformat() if e.timestamp else datetime.now(timezone.utc).isoformat(),
                snapshot_url=frame_url,
            )
        )

    return ResponseEnvelope(success=True, data=output)


@router.get("/{event_id}", response_model=ResponseEnvelope[EventResponse])
async def get_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        eid = uuid.UUID(event_id)
        query = select(Event).options(selectinload(Event.frames)).where(Event.id == eid, Event.tenant_id == current_user.tenant_id)
        event = (await db.execute(query)).scalar_one_or_none()
    except ValueError:
        event = None

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event record not found")

    cname = "Main Perimeter Gate"
    if event.camera_id:
        c_query = select(Camera).where(Camera.id == event.camera_id)
        cam = (await db.execute(c_query)).scalar_one_or_none()
        if cam:
            cname = cam.name

    frame_url = event.frames[0].storage_path if event.frames else "/snapshots/default-event.jpg"

    data = EventResponse(
        id=str(event.id),
        camera_id=str(event.camera_id) if event.camera_id else None,
        camera_name=cname,
        event_type=event.event_type,
        severity=event.severity,
        confidence=event.confidence,
        payload=event.payload or {},
        timestamp=event.timestamp.isoformat() if event.timestamp else datetime.now(timezone.utc).isoformat(),
        snapshot_url=frame_url,
    )
    return ResponseEnvelope(success=True, data=data)
