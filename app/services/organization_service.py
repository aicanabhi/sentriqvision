"""
Organization Service
"""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization


class OrganizationService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ======================================================
    # Create Organization
    # ======================================================

    async def create(self, data: dict):

        # Check duplicate email / organization code
        result = await self.db.execute(
            select(Organization).where(
                or_(
                    Organization.email == data["email"],
                    Organization.organization_code == data["organization_code"],
                )
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization email or organization code already exists.",
            )

        organization = Organization(**data)

        self.db.add(organization)

        await self.db.commit()

        await self.db.refresh(organization)

        return organization

    # ======================================================
    # List Organizations
    # ======================================================

    async def list_organizations(
        self,
        page: int = 1,
        per_page: int = 20,
    ):

        result = await self.db.execute(
            select(Organization)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .order_by(Organization.created_at.desc())
        )

        organizations = result.scalars().all()

        total_result = await self.db.execute(
            select(func.count(Organization.id))
        )

        total = total_result.scalar()

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "organizations": organizations,
        }

    # ======================================================
    # Get Organization
    # ======================================================

    async def get_organization(
        self,
        organization_id: UUID,
    ):

        result = await self.db.execute(
            select(Organization).where(
                Organization.id == str(organization_id)
            )
        )

        organization = result.scalar_one_or_none()

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        return organization

    # ======================================================
    # Update Organization
    # ======================================================

    async def update_organization(
        self,
        organization_id: UUID,
        organization_data,
    ):

        organization = await self.get_organization(
            organization_id
        )

        update_data = organization_data.model_dump(
            exclude_unset=True
        )

        # Duplicate email check
        if "email" in update_data:

            result = await self.db.execute(
                select(Organization).where(
                    Organization.email == update_data["email"],
                    Organization.id != str(organization_id),
                )
            )

            if result.scalar_one_or_none():

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists.",
                )

        # Duplicate organization code check
        if "organization_code" in update_data:

            result = await self.db.execute(
                select(Organization).where(
                    Organization.organization_code
                    == update_data["organization_code"],
                    Organization.id != str(organization_id),
                )
            )

            if result.scalar_one_or_none():

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization code already exists.",
                )

        for key, value in update_data.items():

            setattr(
                organization,
                key,
                value,
            )

        await self.db.commit()

        await self.db.refresh(
            organization
        )

        return organization

    # ======================================================
    # Delete Organization
    # ======================================================

    async def delete_organization(
        self,
        organization_id: UUID,
    ):

        organization = await self.get_organization(
            organization_id
        )

        await self.db.delete(
            organization
        )

        await self.db.commit()

        return True

    # ======================================================
    # Activate
    # ======================================================

    async def activate_organization(
        self,
        organization_id: UUID,
    ):

        organization = await self.get_organization(
            organization_id
        )

        organization.is_active = True

        await self.db.commit()

        await self.db.refresh(
            organization
        )

        return organization

    # ======================================================
    # Deactivate
    # ======================================================

    async def deactivate_organization(
        self,
        organization_id: UUID,
    ):

        organization = await self.get_organization(
            organization_id
        )

        organization.is_active = False

        await self.db.commit()

        await self.db.refresh(
            organization
        )

        return organization

    # ======================================================
    # Count Organizations
    # ======================================================

    async def count_organizations(self):

        result = await self.db.execute(
            select(
                func.count(
                    Organization.id
                )
            )
        )

        return result.scalar()