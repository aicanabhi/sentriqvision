"""
Permission API

RBAC Permission Management
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_super_admin,
)

from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
)

from app.services.permission_service import PermissionService


router = APIRouter()


# ==========================================================
# Create Permission
# ==========================================================


@router.post(
    "",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    permission: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Create new permission.

    Example:
    camera:create
    camera:view
    user:delete
    """

    service = PermissionService(db)

    return await service.create_permission(
        permission
    )


# ==========================================================
# Get All Permissions
# ==========================================================


@router.get(
    "",
    response_model=list[PermissionResponse],
)
async def get_permissions(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Get all permissions.
    """

    service = PermissionService(db)

    return await service.get_permissions()



# ==========================================================
# Get Permission By ID
# ==========================================================


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
)
async def get_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Get permission details.
    """

    service = PermissionService(db)

    return await service.get_permission(
        permission_id
    )



# ==========================================================
# Update Permission
# ==========================================================


@router.put(
    "/{permission_id}",
    response_model=PermissionResponse,
)
async def update_permission(
    permission_id: UUID,
    permission: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Update permission.
    """

    service = PermissionService(db)

    return await service.update_permission(
        permission_id,
        permission,
    )



# ==========================================================
# Delete Permission
# ==========================================================


@router.delete(
    "/{permission_id}",
)
async def delete_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Delete permission.
    """

    service = PermissionService(db)

    await service.delete_permission(
        permission_id
    )

    return {
        "success": True,
        "message": "Permission deleted successfully",
    }



# ==========================================================
# Assign Permission To Role
# ==========================================================


@router.post(
    "/{permission_id}/roles/{role_id}",
)
async def assign_permission_to_role(
    permission_id: UUID,
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Assign permission to role.
    """

    service = PermissionService(db)

    return await service.assign_to_role(
        permission_id,
        role_id,
    )



# ==========================================================
# Remove Permission From Role
# ==========================================================


@router.delete(
    "/{permission_id}/roles/{role_id}",
)
async def remove_permission_from_role(
    permission_id: UUID,
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """
    Remove permission from role.
    """

    service = PermissionService(db)

    await service.remove_from_role(
        permission_id,
        role_id,
    )

    return {
        "success": True,
        "message": "Permission removed from role",
    }