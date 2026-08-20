"""
Resource access management API.
SUPER_ADMIN: Can manage access across all organizations.
ADMIN: Can manage access only within their own organization.
OPERATOR / AUTHORIZED_VIEWER: Cannot grant or revoke resource access.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import AccountRole
from app.database.connection import get_db
from app.models.account import Account
from app.models.camera import Camera
from app.models.site import Site
from app.repositories.account import AccountRepository
from app.repositories.access import AccessRepository
from app.schemas.access import AccessResponse, GrantCameraAccessRequest, GrantSiteAccessRequest
from app.security.authorization import require_roles
from app.services.access import AccessService

router = APIRouter(
    prefix="/auth/access",
    tags=["access management"],
)

@router.post("/sites", response_model=AccessResponse, status_code=status.HTTP_201_CREATED)
async def grant_site_access(
        data: GrantSiteAccessRequest,
        account: Account = Depends(require_roles(AccountRole.SUPER_ADMIN, AccountRole.ADMIN)),
        session: AsyncSession = Depends(get_db),
):
    account_repository = AccountRepository(session)
    access_repository = AccessRepository(session)

    target_account = await account_repository.get_by_id(data.account_id)
    site = await session.get(Site, data.site_id)

    if target_account is None:
        raise HTTPException(status_code=404, detail="Target account not found")

    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    service = AccessService(access_repository)

    try:
        await service.grant_site_access(
            requesting_account=account,
            target_account=target_account,
            site=site,
        )

        await session.commit()

    except PermissionError as exc:
        await session.rollback()
        raise HTTPException(status_code=403, detail=str(exc))

    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=409, detail=str(exc))

    return AccessResponse(
        account_id=target_account.id,
        resource_id=site.id,
        resource_type="SITE"
    )

@router.post("/cameras", response_model=AccessResponse, status_code=status.HTTP_201_CREATED)
async def grant_camera_access(
        data: GrantCameraAccessRequest,
        account=Depends(require_roles(AccountRole.SUPER_ADMIN, AccountRole.ADMIN)),
        session: AsyncSession = Depends(get_db),
):
    account_repository = AccountRepository(session)
    access_repository = AccessRepository(session)

    target_account = await account_repository.get_by_id(data.account_id)
    camera = await session.get(Camera, data.camera_id)

    if target_account is None:
        raise HTTPException(status_code=404, detail="Target account not found")

    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")

    site = await session.get(Site, camera.site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Camera Site not found")
    service = AccessService(access_repository)

    try:
        await service.grant_camera_access(
            requesting_account=account,
            target_account=target_account,
            camera=camera,
            site=site,
        )
        await session.commit()

    except PermissionError as exc:
        await session.rollback()
        raise HTTPException(status_code=403, detail=str(exc))

    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=409, detail=str(exc))

    return AccessResponse(
        account_id=target_account.id,
        resource_id=camera.id,
        resource_type="CAMERA"
    )