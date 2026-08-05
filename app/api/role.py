"""
Role API

Role Management Endpoints
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_org_admin,
    pagination_params,
)
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
)
from app.services.role_service import RoleService

router = APIRouter()


# ==========================================================
# Create Role
# ==========================================================

@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    role: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Create a new role.
    """

    service = RoleService(db)

    return await service.create_role(role)


# ==========================================================
# List Roles
# ==========================================================

@router.get("")
async def list_roles(
    pagination=Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    List all roles.
    """

    service = RoleService(db)

    return await service.list_roles(
        page=pagination["page"],
        per_page=pagination["per_page"],
    )


# ==========================================================
# Get Role
# ==========================================================

@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
async def get_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Get role by ID.
    """

    service = RoleService(db)

    return await service.get_role(role_id)


# ==========================================================
# Update Role
# ==========================================================

@router.put(
    "/{role_id}",
    response_model=RoleResponse,
)
async def update_role(
    role_id: UUID,
    role: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Update role.
    """

    service = RoleService(db)

    return await service.update_role(
        role_id,
        role,
    )


# ==========================================================
# Delete Role
# ==========================================================

@router.delete("/{role_id}")
async def delete_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Delete role.
    """

    service = RoleService(db)

    await service.delete_role(role_id)

    return {
        "success": True,
        "message": "Role deleted successfully",
    }


# ==========================================================
# Assign Permissions
# ==========================================================

@router.post("/{role_id}/permissions")
async def assign_permissions(
    role_id: UUID,
    permission_ids: list[UUID],
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Assign permissions to a role.
    """

    service = RoleService(db)

    return await service.assign_permissions(
        role_id,
        permission_ids,
    )


# ==========================================================
# Remove Permission
# ==========================================================

@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_permission(
    role_id: UUID,
    permission_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Remove permission from role.
    """

    service = RoleService(db)

    return await service.remove_permission(
        role_id,
        permission_id,
    )


# ==========================================================
# Get Role Permissions
# ==========================================================

@router.get("/{role_id}/permissions")
async def get_role_permissions(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Get permissions assigned to a role.
    """

    service = RoleService(db)

    return await service.get_role_permissions(role_id)