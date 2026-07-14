
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.repositories.organization_repository import OrganizationRepository
from app.application.repositories.organization_admin_repository import OrganizationAdminRepository
from app.application.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse, OrganizationStatus
from app.application.schemas.organization_admin import OrganizationAdminCreate, OrganizationAdminResponse
from app.infrastructure.security.hash import get_password_hash
from datetime import datetime


class OrganizationService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = OrganizationRepository(db)
        self.admin_repo = OrganizationAdminRepository(db)

    async def create_organization(self, data: OrganizationCreate, created_by: str) -> OrganizationResponse:
        org_id = await self.repo.create({
            **data.model_dump(),
            "created_by": created_by,
            "updated_by": created_by
        })
        org = await self.repo.get_by_id(org_id)
        return OrganizationResponse(**org)

    async def get_all_organizations(self, skip: int = 0, limit: int = 100) -> List[OrganizationResponse]:
        orgs = await self.repo.get_all(skip=skip, limit=limit)
        return [OrganizationResponse(**org) for org in orgs]

    async def get_organization_by_id(self, org_id: str) -> Optional[OrganizationResponse]:
        org = await self.repo.get_by_id(org_id)
        if org:
            return OrganizationResponse(**org)
        return None

    async def update_organization(self, org_id: str, data: OrganizationUpdate, updated_by: str) -> Optional[OrganizationResponse]:
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = updated_by
        org = await self.repo.update(org_id, update_data)
        if org:
            return OrganizationResponse(**org)
        return None

    async def delete_organization(self, org_id: str) -> bool:
        return await self.repo.delete(org_id)

    async def activate_organization(self, org_id: str, updated_by: str) -> Optional[OrganizationResponse]:
        org = await self.repo.update(org_id, {
            "status": OrganizationStatus.ACTIVE,
            "updated_by": updated_by
        })
        if org:
            return OrganizationResponse(**org)
        return None

    async def suspend_organization(self, org_id: str, updated_by: str) -> Optional[OrganizationResponse]:
        org = await self.repo.update(org_id, {
            "status": OrganizationStatus.SUSPENDED,
            "updated_by": updated_by
        })
        if org:
            return OrganizationResponse(**org)
        return None

    async def create_organization_admin(self, org_id: str, data: OrganizationAdminCreate, created_by: str) -> OrganizationAdminResponse:
        hashed_password = get_password_hash(data.password)
        admin_id = await self.admin_repo.create({
            "email": data.email,
            "name": data.name,
            "phone": data.phone,
            "password": hashed_password,
            "organization_id": org_id,
            "created_by": created_by,
            "updated_by": created_by
        })
        admin = await self.admin_repo.get_by_id(admin_id)
        return OrganizationAdminResponse(**admin)

    async def reset_organization_admin_password(self, admin_id: str, new_password: str, updated_by: str):
        hashed_password = get_password_hash(new_password)
        await self.admin_repo.update(admin_id, {
            "password": hashed_password,
            "updated_by": updated_by
        })
