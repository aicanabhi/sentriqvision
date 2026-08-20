"""
Repository for account-to-resource access assignments.

This layer handles database persistence and queries for:
- account -> site access
- account -> camera access

Organization-level authorization rules belong in the service layer.
"""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account_camera_access import AccountCameraAccess
from app.models.account_site_access import AccountSiteAccess

class AccessRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_site_access(
            self,
            account_id: uuid.UUID,
            site_id: uuid.UUID,
    ) -> AccountSiteAccess | None:
        result = await self.session.execute(
            select(AccountSiteAccess).where(AccountSiteAccess.account_id == account_id, AccountSiteAccess.site_id == site_id))
        return result.scalar_one_or_none()

    async def get_camera_access(
            self,
            account_id: uuid.UUID,
            camera_id: uuid.UUID,
    ) -> AccountCameraAccess | None:
        result = await self.session.execute(
            select(AccountCameraAccess).where(AccountCameraAccess.account_id == account_id, camera_id == camera_id))
        return result.scalar_one_or_none()

    async def grant_site_access(
            self,
            account_id: uuid.UUID,
            site_id: uuid.UUID,
    ) -> AccountSiteAccess:
        access = AccountSiteAccess(account_id=account_id, site_id=site_id)

        self.session.add(access)
        await self.session.flush()

        return access

    async def grant_camera_access(
            self,
            account_id: uuid.UUID,
            camera_id: uuid.UUID,
    ) -> AccountCameraAccess:
        access = AccountCameraAccess(account_id=account_id, camera_id=camera_id)

        self.session.add(access)
        await self.session.flush()

        return access

    async def revoke_site_access(
            self,
            account_id: uuid.UUID,
            site_id: uuid.UUID,
    ) -> bool:
        access = await self.get_site_access(account_id=account_id, site_id=site_id)

        if access is None:
            return False

        await self.session.delete(access)
        await self.session.flush()

        return True

    async def revoke_camera_access(
            self,
            account_id: uuid.UUID,
            camera_id: uuid.UUID,
    ) -> bool:
        access = await self.get_camera_access(account_id=account_id, camera_id=camera_id)

        if access is None:
            return False

        await self.session.delete(access)
        await self.session.flush()

        return True