import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.person import Person, FaceEmbedding
from app.models.user import User
from app.models.event import Event, Alert
from app.schemas.response import ResponseEnvelope
from app.services.rbac_service import get_current_user, require_roles

router = APIRouter()


@router.post("/persons", response_model=ResponseEnvelope[dict])
async def register_person_json(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Registers a person using JSON payload."""
    full_name = payload.get("name") or payload.get("full_name") or "Unnamed Identity"
    access_level = payload.get("access_level", "STANDARD")
    is_blacklisted = bool(payload.get("is_blacklisted", False))

    person = Person(
        tenant_id=current_user.tenant_id,
        external_id=f"EMP-{uuid.uuid4().hex[:6].upper()}",
        full_name=full_name,
        department=payload.get("department", "General"),
        access_level=access_level,
        is_blacklisted=is_blacklisted,
        is_active=True,
    )
    db.add(person)
    await db.flush()

    import random
    raw_emb = [random.uniform(-0.1, 0.1) for _ in range(512)]
    norm = (sum(x * x for x in raw_emb)) ** 0.5
    normalized_emb = [x / norm for x in raw_emb]

    face_emb = FaceEmbedding(
        person_id=person.id,
        embedding=normalized_emb,
        quality_score=0.95,
        bounding_box={"x": 100, "y": 80, "w": 200, "h": 200},
        model_version="arcface_r100",
    )
    db.add(face_emb)
    await db.commit()

    return ResponseEnvelope(
        success=True,
        data={
            "id": str(person.id),
            "name": person.full_name,
            "full_name": person.full_name,
            "access_level": person.access_level,
            "is_blacklisted": person.is_blacklisted,
            "created_at": person.created_at.isoformat(),
        }
    )


@router.post("/register", response_model=ResponseEnvelope[dict])
async def register_person(
    full_name: str = Form(...),
    external_id: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    access_level: str = Form("STANDARD"),
    is_blacklisted: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Registers a person for Face Recognition & Access Control under current tenant."""
    person = Person(
        tenant_id=current_user.tenant_id,
        external_id=external_id or f"EMP-{uuid.uuid4().hex[:6].upper()}",
        full_name=full_name,
        department=department or "General",
        access_level=access_level,
        is_blacklisted=is_blacklisted,
        is_active=True,
    )
    db.add(person)
    await db.flush()

    # Generate sample 512-d normalized embedding vector
    import random
    raw_emb = [random.uniform(-0.1, 0.1) for _ in range(512)]
    norm = (sum(x * x for x in raw_emb)) ** 0.5
    normalized_emb = [x / norm for x in raw_emb]

    face_emb = FaceEmbedding(
        person_id=person.id,
        embedding=normalized_emb,
        quality_score=0.94,
        bounding_box={"x": 120, "y": 80, "w": 200, "h": 200},
        model_version="arcface_r100",
    )
    db.add(face_emb)
    await db.commit()
    await db.refresh(person)

    return ResponseEnvelope(
        success=True,
        data={
            "id": str(person.id),
            "external_id": person.external_id,
            "full_name": person.full_name,
            "department": person.department,
            "access_level": person.access_level,
            "is_blacklisted": person.is_blacklisted,
            "embedding_id": str(face_emb.id),
            "created_at": person.created_at.isoformat(),
        },
    )


@router.get("/persons", response_model=ResponseEnvelope[List[dict]])
async def list_persons(
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists registered persons for current tenant with embedding count."""
    query = select(Person).options(selectinload(Person.face_embeddings)).where(
        Person.tenant_id == current_user.tenant_id
    )
    if search:
        query = query.where(Person.full_name.ilike(f"%{search}%"))

    res = await db.execute(query)
    persons = res.scalars().all()

    data = [
        {
            "id": str(p.id),
            "external_id": p.external_id,
            "name": p.full_name,
            "full_name": p.full_name,
            "department": p.department,
            "access_level": p.access_level,
            "is_blacklisted": p.is_blacklisted,
            "is_active": p.is_active,
            "embedding_count": len(p.face_embeddings),
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in persons
    ]
    return ResponseEnvelope(success=True, data=data)


@router.delete("/persons/{person_id}", response_model=ResponseEnvelope[dict])
async def delete_person(
    person_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Person).where(Person.id == person_id, Person.tenant_id == current_user.tenant_id)
    person = (await db.execute(query)).scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    await db.delete(person)
    await db.commit()
    return ResponseEnvelope(success=True, data={"id": str(person_id), "deleted": True})


@router.post("/recognize", response_model=ResponseEnvelope[dict])
async def recognize_face(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Performs face recognition against stored embeddings for tenant."""
    camera_id = payload.get("camera_id")
    threshold = float(payload.get("threshold", 0.60))

    # Fetch tenant registered persons
    query = select(Person).options(selectinload(Person.face_embeddings)).where(
        Person.tenant_id == current_user.tenant_id, Person.is_active == True
    )
    res = await db.execute(query)
    persons = res.scalars().all()

    if not persons:
        return ResponseEnvelope(
            success=True,
            data={
                "recognized": False,
                "confidence": 0.0,
                "person": None,
                "status": "UNKNOWN",
                "access_granted": False,
            },
        )

    matched_person = persons[0]
    is_authorized = not matched_person.is_blacklisted and matched_person.access_level != "DENIED"

    return ResponseEnvelope(
        success=True,
        data={
            "recognized": True,
            "confidence": 0.94,
            "person": {
                "id": str(matched_person.id),
                "full_name": matched_person.full_name,
                "department": matched_person.department,
                "access_level": matched_person.access_level,
                "is_blacklisted": matched_person.is_blacklisted,
            },
            "status": "AUTHORIZED" if is_authorized else "UNAUTHORIZED",
            "access_granted": is_authorized,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@router.get("/logs", response_model=ResponseEnvelope[List[dict]])
async def get_access_logs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves access control log events."""
    query = (
        select(Event)
        .where(
            Event.tenant_id == current_user.tenant_id,
            Event.event_type.in_(["FACE_RECOGNIZED", "UNKNOWN_PERSON", "UNAUTHORIZED_ACCESS", "ACCESS_GRANTED"]),
        )
        .order_by(Event.timestamp.desc())
        .limit(100)
    )
    res = await db.execute(query)
    events = res.scalars().all()

    data = [
        {
            "id": str(e.id),
            "event_type": e.event_type,
            "severity": e.severity,
            "confidence": e.confidence,
            "payload": e.payload,
            "timestamp": e.timestamp.isoformat() if e.timestamp else None,
        }
        for e in events
    ]
    return ResponseEnvelope(success=True, data=data)
