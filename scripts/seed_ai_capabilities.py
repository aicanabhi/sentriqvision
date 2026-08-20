import asyncio
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal, engine
from app.models.ai_parameter import AIParameterCatalog, OrganizationAIParameter
from app.models.organization import Organization
from app.services.parameter_service import ParameterService, CANONICAL_54_SERVICES


async def main():
    print("=" * 60)
    print("SentriqVision 54 - Seeding AI Capability Master Catalog")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        try:
            service = ParameterService(db)
            print("1. Synchronizing Catalog and Existing Organization Entitlements...")
            await service.seed_catalog_and_org_entitlements()
            await db.commit()

            # 2. Verify Catalog Count
            cat_count_res = await db.execute(select(func.count(AIParameterCatalog.id)))
            catalog_count = cat_count_res.scalar()

            print(f"Catalog Status: {catalog_count}/54 Canonical Capabilities Active")

            if catalog_count != 54:
                print(f"ERROR: Catalog count mismatch! Expected 54, found {catalog_count}")
                sys.exit(1)

            # 3. Verify Organization Entitlements
            orgs_res = await db.execute(select(Organization))
            orgs = orgs_res.scalars().all()
            print(f"\n2. Verifying Organization Entitlements across {len(orgs)} Organization(s):")

            all_valid = True
            for org in orgs:
                org_ent_res = await db.execute(
                    select(func.count(OrganizationAIParameter.id)).where(
                        OrganizationAIParameter.organization_id == org.id
                    )
                )
                org_count = org_ent_res.scalar()
                status = "OK" if org_count == 54 else "INCOMPLETE"
                print(f" - Organization: '{org.name}' ({org.id}): {org_count}/54 entitlements [{status}]")
                if org_count != 54:
                    all_valid = False

            if not all_valid:
                print("\nERROR: One or more organizations do not have 54 entitlement records.")
                sys.exit(1)

            print("\nSUCCESS: All 54 canonical AI capabilities seeded and isolated per organization.")
            print("=" * 60)

        except Exception as e:
            print(f"\nFATAL: Seeding failed with exception: {e}")
            await db.rollback()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
