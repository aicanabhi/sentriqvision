import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.schemas.zone import ZoneCreate, ZoneResponse
from app.services.zone import ZoneService
from app.auth import AccountRole
from app.models.site import Site
from app.security.authorization import require_roles

router = APIRouter(
    prefix="/zones",
    tags=["zones"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# List all zones
@router.get("/", response_model=list[ZoneResponse])
async def list_zones(
    session: AsyncSession = Depends(get_db)):
    service = ZoneService(session)
    return await service.get_all()

# Get zones belonging to a site
@router.get("/site/{site_id}", response_model=list[ZoneResponse])
async def list_zones_by_site(
        site_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = ZoneService(session)
    return await service.get_by_site(site_id)

# Get one zone
@router.get("/{zone_id}", response_model=ZoneResponse)
async def get_zone(
        zone_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = ZoneService(session)
    zone = await service.get_by_id(zone_id)

    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

# Create zone
@router.post("/", response_model=ZoneResponse)
async def create_zone(
        data: ZoneCreate,
        account=Depends(require_roles(AccountRole.SUPER_ADMIN, AccountRole.ADMIN)),
        session: AsyncSession = Depends(get_db),
):
    site = await session.get(Site, data.site_id)

    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    if (
        account.role == AccountRole.ADMIN.value and
        site.organization_id != account.organization_id
    ):
        raise HTTPException(status_code=403, detail="Cannot create a zone outside your organization")

    service = ZoneService(session)

    try:
        zone = await service.create(
            site_id=data.site_id,
            name=data.name,
            zone_type=data.zone_type,
            status=data.status,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    await session.commit()
    await session.refresh(zone)

    return zone

# Delete zone
@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(
        zone_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = ZoneService(session)

    zone = await service.get_by_id(zone_id)

    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")

    await service.delete(zone_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)