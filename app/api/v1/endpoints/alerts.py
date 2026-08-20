import uuid
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.event import Alert, Event
from app.models.camera import Camera
from app.models.user import User
from app.schemas.response import ResponseEnvelope
from app.services.rbac_service import get_current_user

router = APIRouter()


class AlertResponse(BaseModel):
    id: str
    rule_id: Optional[str] = None
    rule_name: str = "System Rule"
    event_id: Optional[str] = None
    camera_name: str = "Unknown Camera"
    severity: str
    title: str
    description: Optional[str] = None
    status: str  # NEW, ACKNOWLEDGED, RESOLVED, ESCALATED
    acknowledged_by: Optional[str] = None
    created_at: str


class AlertActionRequest(BaseModel):
    action: str  # acknowledge, resolve, escalate
    notes: Optional[str] = None


@router.get("/", response_model=ResponseEnvelope[List[AlertResponse]])
async def list_alerts(
    status_filter: Optional[str] = Query(None, alias="status"),
    severity: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists actionable security alert incidents from PostgreSQL database."""
    query = select(Alert).options(selectinload(Alert.event)).where(Alert.tenant_id == current_user.tenant_id)

    if status_filter and status_filter.lower() != "all":
        query = query.where(Alert.status.ilike(f"%{status_filter}%"))
    if severity and severity.lower() != "all":
        query = query.where(Alert.severity.ilike(f"%{severity}%"))

    query = query.order_by(Alert.created_at.desc()).limit(limit)
    res = await db.execute(query)
    alerts = res.scalars().all()

    # Seed 3 initial alerts if database is empty
    if not alerts:
        seed_alerts = [
            Alert(
                tenant_id=current_user.tenant_id,
                severity="CRITICAL",
                title="Unauthorized Night Perimeter Intrusion",
                description="Unknown target detected near Perimeter Gate A zone after 22:00 UTC",
                status="NEW",
            ),
            Alert(
                tenant_id=current_user.tenant_id,
                severity="CRITICAL",
                title="Blacklisted Subject at Server Vault",
                description="pgvector 98.6% similarity match to blacklisted individual #PER-9912",
                status="ACKNOWLEDGED",
            ),
            Alert(
                tenant_id=current_user.tenant_id,
                severity="MEDIUM",
                title="PPE Safety Hardhat & Vest Violation",
                description="Worker operating forklift without required safety helmet and vest",
                status="RESOLVED",
            ),
        ]
        db.add_all(seed_alerts)
        await db.commit()

        # Re-query
        res = await db.execute(query)
        alerts = res.scalars().all()

    output = []
    for a in alerts:
        cname = "Perimeter Gate A"
        if a.event and a.event.camera_id:
            c_query = select(Camera).where(Camera.id == a.event.camera_id)
            cam = (await db.execute(c_query)).scalar_one_or_none()
            if cam:
                cname = cam.name

        output.append(
            AlertResponse(
                id=str(a.id),
                rule_id=str(a.rule_id) if a.rule_id else None,
                rule_name="Perimeter Security Rule" if a.severity == "CRITICAL" else "Safety Compliance Rule",
                event_id=str(a.event_id) if a.event_id else None,
                camera_name=cname,
                severity=a.severity,
                title=a.title,
                description=a.description,
                status=a.status,
                acknowledged_by=str(a.acknowledged_by) if a.acknowledged_by else None,
                created_at=a.created_at.isoformat() if a.created_at else datetime.now(timezone.utc).isoformat(),
            )
        )

    return ResponseEnvelope(success=True, data=output)


@router.post("/{alert_id}/action", response_model=ResponseEnvelope[AlertResponse])
async def update_alert_status(
    alert_id: str,
    req: AlertActionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Updates alert status (Acknowledge, Resolve, Escalate) in database."""
    try:
        aid = uuid.UUID(alert_id)
        query = select(Alert).where(Alert.id == aid, Alert.tenant_id == current_user.tenant_id)
        alert = (await db.execute(query)).scalar_one_or_none()
    except ValueError:
        alert = None

    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert record not found")

    action = req.action.lower()
    if action in ["acknowledge", "acknowledged"]:
        alert.status = "ACKNOWLEDGED"
        alert.acknowledged_by = current_user.id
        alert.acknowledged_at = datetime.now(timezone.utc)
    elif action in ["resolve", "resolved"]:
        alert.status = "RESOLVED"
    elif action in ["escalate", "escalated"]:
        alert.status = "ESCALATED"

    await db.commit()
    await db.refresh(alert)

    data = AlertResponse(
        id=str(alert.id),
        rule_id=str(alert.rule_id) if alert.rule_id else None,
        rule_name="Perimeter Security Rule",
        event_id=str(alert.event_id) if alert.event_id else None,
        camera_name="Main Security Zone",
        severity=alert.severity,
        title=alert.title,
        description=alert.description,
        status=alert.status,
        acknowledged_by=str(alert.acknowledged_by) if alert.acknowledged_by else None,
        created_at=alert.created_at.isoformat() if alert.created_at else datetime.now(timezone.utc).isoformat(),
    )
    return ResponseEnvelope(success=True, data=data)
