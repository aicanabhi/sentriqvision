import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from app.database.connection import AsyncSessionLocal
from app.schemas.site import SiteCreate, SiteResponse
from app.services.site import SiteService
from app.auth import AccountRole
from app.security.authorization import require_roles

router = APIRouter(
    prefix="/sites",
    tags=["sites"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model=list[SiteResponse])
async def list_sites(
        session: AsyncSession = Depends(get_db),
):
    service = SiteService(session)
    return await service.get_all()

@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(
        site_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = SiteService(session)
    site = await service.get_by_id(site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/", response_model=SiteResponse)
async def create_site(
        data: SiteCreate,
        account=Depends(require_roles(AccountRole.SUPER_ADMIN, AccountRole.ADMIN)),
        session: AsyncSession = Depends(get_db),
):

    # Organization Admins can only create sites inside their own organization.
    if (
        account.role == AccountRole.ADMIN.value and
        data.organization_id != account.organization_id
    ):
        raise HTTPException(status_code=403, detail="Cannot create a site outside your organization")

    service = SiteService(session)

    try:
        site = await service.create(
            organization_id=data.organization_id,
            name=data.name,
            timezone=data.timezone,
            status=data.status,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    await session.commit()
    await session.refresh(site)
    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(
        site_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):

    service = SiteService(session)

    site = await service.get_by_id(site_id)

    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    await service.delete(site_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)