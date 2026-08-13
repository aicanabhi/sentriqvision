from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal
from app.services.organization import OrganizationService
from app.schemas.organization import OrganizationCreate
import uuid


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/")
async def list_organizations(session: AsyncSession = Depends(get_db)):
    service = OrganizationService(session)

    return await service.get_all()

@router.post("/")
async def create_organization(
        data: OrganizationCreate,
        session: AsyncSession = Depends(get_db)
    ):
    service = OrganizationService(session)
    organization = await service.create(
        name=data.name,
        status=data.status,
    )

    await session.commit()
    return organization

@router.get("/{organization_id}")
async def get_organization(
    organization_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    service = OrganizationService(session)

    organization = await service.get_by_id(organization_id)

    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    return organization

@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
        organization_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
):
    service = OrganizationService(session)
    organization = await service.get_by_id(organization_id)
    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )
    await session.delete(organization)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
