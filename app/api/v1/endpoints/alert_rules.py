import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.event import AlertRule
from app.models.user import User
from app.schemas.response import ResponseEnvelope
from app.services.rbac_service import get_current_user

router = APIRouter()


class AlertRuleCreate(BaseModel):
    name: str
    event_type: str
    camera_id: Optional[str] = None
    severity: str = "HIGH"
    condition_json: Dict[str, Any] = {}
    actions_json: List[str] = []
    is_enabled: bool = True


class AlertRuleResponse(BaseModel):
    id: str
    name: str
    event_type: str
    camera_id: Optional[str] = None
    severity: str
    condition_json: Dict[str, Any]
    actions_json: List[str]
    is_enabled: bool
    created_at: str


@router.get("/", response_model=ResponseEnvelope[List[AlertRuleResponse]])
async def list_alert_rules(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists tenant alert rules from PostgreSQL database."""
    query = select(AlertRule).where(AlertRule.tenant_id == current_user.tenant_id)
    res = await db.execute(query)
    rules = res.scalars().all()

    # Seed an initial rule if empty
    if not rules:
        seed_rule = AlertRule(
            tenant_id=current_user.tenant_id,
            name="After Hours Perimeter Intrusion Rule",
            event_type="INTRUSION_DETECTED",
            severity="CRITICAL",
            condition_json={"min_confidence": 0.85, "time_window": ["22:00", "06:00"]},
            actions_json=["PUSH_NOTIFICATION", "DISPATCH_SECURITY"],
            is_enabled=True,
        )
        db.add(seed_rule)
        await db.commit()
        res = await db.execute(query)
        rules = res.scalars().all()

    output = [
        AlertRuleResponse(
            id=str(r.id),
            name=r.name,
            event_type=r.event_type,
            severity=r.severity,
            condition_json=r.condition_json or {},
            actions_json=r.actions_json if isinstance(r.actions_json, list) else [],
            is_enabled=r.is_enabled,
            created_at=r.created_at.isoformat() if r.created_at else datetime.now(timezone.utc).isoformat(),
        )
        for r in rules
    ]
    return ResponseEnvelope(success=True, data=output)


@router.post("/", response_model=ResponseEnvelope[AlertRuleResponse], status_code=status.HTTP_201_CREATED)
async def create_alert_rule(
    rule: AlertRuleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Creates new tenant alert rule in PostgreSQL database."""
    new_rule = AlertRule(
        tenant_id=current_user.tenant_id,
        name=rule.name,
        event_type=rule.event_type,
        severity=rule.severity,
        condition_json=rule.condition_json,
        actions_json=rule.actions_json,
        is_enabled=rule.is_enabled,
    )
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)

    data = AlertRuleResponse(
        id=str(new_rule.id),
        name=new_rule.name,
        event_type=new_rule.event_type,
        severity=new_rule.severity,
        condition_json=new_rule.condition_json or {},
        actions_json=new_rule.actions_json if isinstance(new_rule.actions_json, list) else [],
        is_enabled=new_rule.is_enabled,
        created_at=new_rule.created_at.isoformat() if new_rule.created_at else datetime.now(timezone.utc).isoformat(),
    )
    return ResponseEnvelope(success=True, data=data)


@router.patch("/{rule_id}/toggle", response_model=ResponseEnvelope[AlertRuleResponse])
@router.put("/{rule_id}/toggle", response_model=ResponseEnvelope[AlertRuleResponse])
async def toggle_rule(
    rule_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggles active state of an alert rule in database."""
    try:
        rid = uuid.UUID(rule_id)
        query = select(AlertRule).where(AlertRule.id == rid, AlertRule.tenant_id == current_user.tenant_id)
        rule = (await db.execute(query)).scalar_one_or_none()
    except ValueError:
        rule = None

    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert rule not found")

    rule.is_enabled = not rule.is_enabled
    await db.commit()
    await db.refresh(rule)

    data = AlertRuleResponse(
        id=str(rule.id),
        name=rule.name,
        event_type=rule.event_type,
        severity=rule.severity,
        condition_json=rule.condition_json or {},
        actions_json=rule.actions_json if isinstance(rule.actions_json, list) else [],
        is_enabled=rule.is_enabled,
        created_at=rule.created_at.isoformat() if rule.created_at else datetime.now(timezone.utc).isoformat(),
    )
    return ResponseEnvelope(success=True, data=data)
