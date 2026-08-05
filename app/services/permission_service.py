"""
Permission Service

Business logic for Permission Management
"""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission, PermissionCategory
from app.models.role import Role
from app.models.role_permission import RolePermission


class PermissionService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================================================
    # Create Permission
    # ==========================================================

    async def create_permission(self, permission_data):

        existing = await self.db.execute(
            select(Permission).where(
                Permission.code == permission_data.code
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission code already exists",
            )

        permission = Permission(
            name=permission_data.name,
            code=permission_data.code,
            display_name=permission_data.display_name,
            description=permission_data.description,
            category=PermissionCategory(permission_data.category),
            module=permission_data.module,
            action=permission_data.action,
        )

        self.db.add(permission)

        await self.db.commit()
        await self.db.refresh(permission)

        return permission

    # ==========================================================
    # List Permissions
    # ==========================================================

    async def get_permissions(self):

        result = await self.db.execute(
            select(Permission)
        )

        return result.scalars().all()

    # ==========================================================
    # Get Permission
    # ==========================================================

    async def get_permission(
        self,
        permission_id: UUID,
    ):

        result = await self.db.execute(
            select(Permission).where(
                Permission.id == str(permission_id)
            )
        )

        permission = result.scalar_one_or_none()

        if permission is None:
            raise HTTPException(
                status_code=404,
                detail="Permission not found",
            )

        return permission

    # ==========================================================
    # Update Permission
    # ==========================================================

    async def update_permission(
        self,
        permission_id: UUID,
        permission_data,
    ):

        permission = await self.get_permission(permission_id)

        data = permission_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for key, value in data.items():

            if key == "category":
                value = PermissionCategory(value)

            if hasattr(permission, key):
                setattr(permission, key, value)

        await self.db.commit()
        await self.db.refresh(permission)

        return permission

    # ==========================================================
    # Delete Permission
    # ==========================================================

    async def delete_permission(
        self,
        permission_id: UUID,
    ):

        permission = await self.get_permission(permission_id)

        await self.db.delete(permission)

        await self.db.commit()

        return True

    # ==========================================================
    # Assign Permission To Role
    # ==========================================================

    async def assign_to_role(
        self,
        permission_id: UUID,
        role_id: UUID,
    ):

        permission = await self.get_permission(permission_id)

        role_result = await self.db.execute(
            select(Role).where(
                Role.id == str(role_id)
            )
        )

        role = role_result.scalar_one_or_none()

        if role is None:
            raise HTTPException(
                status_code=404,
                detail="Role not found",
            )

        mapping_result = await self.db.execute(
            select(RolePermission).where(
                RolePermission.role_id == str(role_id),
                RolePermission.permission_id == str(permission_id),
            )
        )

        mapping = mapping_result.scalar_one_or_none()

        if mapping:
            return {
                "success": True,
                "message": "Permission already assigned",
            }

        mapping = RolePermission(
            role_id=str(role_id),
            permission_id=str(permission_id),
            allowed=True,
        )

        self.db.add(mapping)

        await self.db.commit()

        return {
            "success": True,
            "message": "Permission assigned successfully",
        }

    # ==========================================================
    # Remove Permission From Role
    # ==========================================================

    async def remove_from_role(
        self,
        permission_id: UUID,
        role_id: UUID,
    ):

        result = await self.db.execute(
            select(RolePermission).where(
                RolePermission.role_id == str(role_id),
                RolePermission.permission_id == str(permission_id),
            )
        )

        mapping = result.scalar_one_or_none()

        if mapping is None:
            raise HTTPException(
                status_code=404,
                detail="Permission mapping not found",
            )

        await self.db.delete(mapping)

        await self.db.commit()

        return True