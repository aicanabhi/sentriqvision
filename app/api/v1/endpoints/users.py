from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User
from app.schemas.response import ResponseEnvelope
from app.schemas.user import UserResponse
from app.services.rbac_service import get_current_user, require_roles

router = APIRouter()


import uuid
from typing import Dict, Any, Optional
from fastapi import HTTPException

from app.models.ai_parameter import AuditLog


@router.get("/me", response_model=ResponseEnvelope[UserResponse])
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return ResponseEnvelope(success=True, data=UserResponse.model_validate(current_user))


@router.get("/", response_model=ResponseEnvelope[List[UserResponse]])
async def list_tenant_users(
    current_user: User = Depends(require_roles(["SUPER_ADMIN", "TENANT_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(User)
        .options(selectinload(User.roles))
        .where(User.tenant_id == current_user.tenant_id)
    )
    result = await db.execute(query)
    users = result.scalars().all()
    data = [UserResponse.model_validate(u) for u in users]
    return ResponseEnvelope(success=True, data=data)


@router.post("/{user_id}/activate", response_model=ResponseEnvelope[dict])
async def activate_user(
    user_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN", "TENANT_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Activates a user account."""
    query = select(User).where(User.id == user_id)
    if not current_user.is_superuser:
        query = query.where(User.tenant_id == current_user.tenant_id)
    user = (await db.execute(query)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    audit = AuditLog(
        organization_id=None,
        user_id=current_user.id,
        action="ACTIVATE_USER",
        resource_type="user",
        resource_id=str(user.id),
        details={"email": user.email}
    )
    db.add(audit)
    await db.commit()
    return ResponseEnvelope(success=True, data={"id": str(user_id), "is_active": True})


@router.post("/{user_id}/deactivate", response_model=ResponseEnvelope[dict])
async def deactivate_user(
    user_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN", "TENANT_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Deactivates a user account."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")

    query = select(User).where(User.id == user_id)
    if not current_user.is_superuser:
        query = query.where(User.tenant_id == current_user.tenant_id)
    user = (await db.execute(query)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    audit = AuditLog(
        organization_id=None,
        user_id=current_user.id,
        action="DEACTIVATE_USER",
        resource_type="user",
        resource_id=str(user.id),
        details={"email": user.email}
    )
    db.add(audit)
    await db.commit()
    return ResponseEnvelope(success=True, data={"id": str(user_id), "is_active": False})


@router.delete("/{user_id}", response_model=ResponseEnvelope[dict])
async def delete_user(
    user_id: uuid.UUID,
    current_user: User = Depends(require_roles(["SUPER_ADMIN", "TENANT_ADMIN"])),
    db: AsyncSession = Depends(get_db),
):
    """Deletes a user account."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    query = select(User).where(User.id == user_id)
    if not current_user.is_superuser:
        query = query.where(User.tenant_id == current_user.tenant_id)
    user = (await db.execute(query)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.email
    await db.delete(user)

    audit = AuditLog(
        organization_id=None,
        user_id=current_user.id,
        action="DELETE_USER",
        resource_type="user",
        resource_id=str(user_id),
        details={"email": email}
    )
    db.add(audit)
    await db.commit()
    return ResponseEnvelope(success=True, data={"id": str(user_id), "email": email, "deleted": True})
