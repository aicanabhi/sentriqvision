"""
Access service.
Enforces organization boundaries when assigning and checking access.

RULES:
SUPER_ADMIN: Full platform access.
ADMIN: Full access within their organization.
OPERATOR/AUTHORIZED VIEWER: Access only through explicit site or camera assignments.
Cross-organization access: Always denied.
"""

import uuid
from sqlalchemy import select
from app.auth import AccountRole
from app.models.account import Account
from app.models.camera import Camera
from app.models.site import Site
from app.repositories.access import AccessRepository

class AccessService:
    def __init__(self, repository: AccessRepository):
        self.repository = repository

    # ROLE HELPERS
    @staticmethod
    def is_super_admin(account: Account) -> bool:
        return account.role == AccountRole.SUPER_ADMIN.value

    @staticmethod
    def is_admin(account: Account) -> bool:
        return account.role == AccountRole.ADMIN.value

    @staticmethod
    def is_resource_user(account: Account) -> bool:
        return account.role in {
            AccountRole.OPERATOR.value,
            AccountRole.AUTHORIZED_VIEWER.value,
        }

    # ASSIGNMENT AUTHORIZATION
    @staticmethod
    def _can_manage_access(
            requesting_account: Account,
            target_account: Account,
    )->bool:
        """
        Determine whether requesting_account can manage resource access for target_account.
        """
        if not requesting_account.is_active:
            return False

        if not target_account.is_active:
            return False

        if not AccessService.is_resource_user(target_account):
            return False

        # Super Admin can manage resource users anywhere.
        if AccessService.is_super_admin(requesting_account):
            return True

        # Organization Admin can only manage accounts belonging to their own organization.
        if AccessService.is_admin(requesting_account):
            return(requesting_account.organization_id == target_account.organization_id)
        return False

    # Grant site access
    async def grant_site_access(
            self,
            requesting_account: Account,
            target_account: Account,
            site: Site,
    ):
        """
        Grant target_account access to a site.

        Site access grants access to all cameras belonging
        to that site.
        """

        if not self._can_manage_access(requesting_account, target_account):
            raise PermissionError("Account is not authorized to manage this access")

        # Super Admin may operate across organizations.
        # Organization Admin must remain inside their organization.

        if (
            self.is_admin(requesting_account) and
            requesting_account.organization_id != site.organization_id
        ):
            raise PermissionError("Cannot grant access to a site outside your organization.")

        # Target account must belong to the site's organization.
        if target_account.organization_id != site.organization_id:
            raise PermissionError("Target account and site belong to different organizations.")

        existing = await self.repository.get_site_access(target_account.id, site.id)

        if existing:
            raise ValueError("Site access already exists.")

        return await self.repository.grant_site_access(target_account.id, site.id)

    # Grant camera access
    async def grant_camera_access(
            self,
            requesting_account: Account,
            target_account: Account,
            camera: Camera,
            site: Site,
    ):
        """
        Grant target_account access to a camera.
        """
        if not self._can_manage_access(requesting_account, target_account):
            raise PermissionError("Account is not authorized to manage this access.")

        # Verify camera really belongs to the supplied site.
        if camera.site_id != site.id:
            raise ValueError("Camera does not belong to the specified site.")

        # Organization Admin must stay within their organization.
        if (
            self.is_admin(requesting_account) and
        requesting_account.organization_id != site.organization_id
        ):
            raise PermissionError("Cannot grant access to a camera outside your organization.")

        # Target account and camera must belong to the same organization.
        if target_account.organization_id != site.organization_id:
            raise PermissionError("Target account and camera belong to different organizations.")

        existing = await self.repository.get_camera_access(target_account.id, camera.id)
        if existing:
            raise ValueError("Camera access already exists.")

        return await self.repository.grant_camera_access(target_account.id, camera.id)

    # Resource access checks
    async def has_site_access(
            self,
            account: Account,
            site_id: uuid.UUID,
            site_organization_id: uuid.UUID,
    ) -> bool:

        if not account.is_active:
            return False

        if self.is_super_admin(account):
            return True

        if account.organization_id != site_organization_id:
            return False

        if self.is_admin(account):
            return True

        access = await self.repository.get_site_access(account.id, site_id,)
        return access is not None

    async def has_camera_access(
            self,
            account: Account,
            camera_id: uuid.UUID,
            camera_site_id: uuid.UUID,
            camera_site_organization_id: uuid.UUID,
    ) -> bool:

        if not account.is_active:
            return False

        if self.is_super_admin(account):
            return True

        if account.organization_id != camera_site_organization_id:
            return False

        if self.is_admin(account):
            return True

        # Direct camera assignment
        camera_access = await self.repository.get_camera_access(account.id, camera_id,)
        if camera_access is not None:
            return True

        # Site assignment grants acces to camera in that site
        site_access = await self.repository.get_site_access(account.id, camera_site_id,)
        return site_access is not None

    # Revoke acces
    async def revoke_site_access(
            self,
            requesting_account: Account,
            target_account: Account,
            site: Site,
    ) -> bool:

        if not self._can_manage_access(requesting_account, target_account):
            raise PermissionError("Account is not authorized to manage this access.")

        if target_account.organization_id != site.organization_id:
            raise PermissionError("Target account and site belong to different organizations.")

        return await self.repository.revoke_site_access(target_account.id, site.id)

    async def revoke_camera_access(
            self,
            requesting_account: Account,
            target_account: Account,
            camera: Camera,
            site: Site,
    ) -> bool:

        if not self._can_manage_access(requesting_account, target_account):
            raise PermissionError("Account is not authorized to manage this access.")

        if camera.site_id != site_id:
            raise ValueError("Camera does not belong to the specified site.")

        if target_account.organization_id != site.organization_id:
            raise PermissionError("Target account and camera belong to different organizations.")

        return await self.repository.revoke_camera_access(target_account.id, camera.id)