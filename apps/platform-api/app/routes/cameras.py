import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from app.database.connection import AsyncSessionLocal
from app.schemas.camera import CameraCreate, CameraResponse
from app.services.camera import CameraService
from app.auth import AccountRole
from app.models.site import Site
from app.security.authorization import require_roles

router = APIRouter(
    tags=["cameras"],
    prefix="/cameras",
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# List all cameras
@router.get("/", response_model=list[CameraResponse])
async def list_cameras(session: AsyncSession = Depends(get_db)):
    service = CameraService(session)
    return await service.get_all()

# List cameras belonging to a site
@router.get("/site/{site_id}", response_model=list[CameraResponse])
async def list_cameras_by_site(
        site_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraService(session)
    return await service.get_by_site(site_id)

# List cameras belonging to a zone
@router.get("/zone/{zone_id}", response_model=list[CameraResponse])
async def list_cameras_by_zone(
        zone_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraService(session)
    return await service.get_by_zone(zone_id)

# Get one camera
@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(
        camera_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraService(session)
    camera = await service.get_by_id(camera_id)

    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

# Create camera
@router.post("/", response_model=CameraResponse)
async def create_camera(
        data: CameraCreate,
        account=Depends(require_roles(AccountRole.SUPER_ADMIN, AccountRole.ADMIN)),
        session: AsyncSession = Depends(get_db),
):
    # The site is the source of truth for organization ownership.
    site = await session.get(Site, data.site_id)

    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    # Organization Admins may only create cameras on site belonging to their
    # organization.
    if(
        account.role == AccountRole.ADMIN.value and
        site.organization_id != account.organization_id
    ):
        raise HTTPException(status_code=403, detail="Cannot create a camera outside your organization")

    service = CameraService(session)

    try:
        camera = await service.create(
            site_id=data.site_id,
            zone_id=data.zone_id,
            camera_code=data.camera_code,
            name=data.name,
            rtsp_url=data.rtsp_url,
            resolution=data.resolution,
            fps=data.fps,
            status=data.status,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    await session.commit()
    await session.refresh(camera)
    return camera

# Delete camera
@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(
        camera_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = CameraService(session)

    camera = await service.get_by_id(camera_id)

    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    await service.delete(camera_id)

    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)