"""
Update the existing SentriqVision Super Admin account.

This script updates:
    - Super Admin email
    - Super Admin password

It never creates a second Super Admin and never assigns the
Super Admin to an organization.
"""

import asyncio
import getpass
from sqlalchemy import select
from app.auth import AccountRole
from app.database.connection import AsyncSessionLocal
from app.models.account import Account
from app.security.password import hash_password

async def update_super_admin() -> None:

    new_email = input("New Super Admin email: ").strip().lower()
    new_password = input("New Super Admin password: ")
    confirm_password = input("Confirm new password: ")

    if new_password != confirm_password:
        raise ValueError("Passwords do not match")

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Account).where(Account.role == AccountRole.SUPER_ADMIN.value)
        )

        super_admin = result.scalar_one_or_none()

        if super_admin is None:
            raise ValueError("Super Admin does not exist")

        # Prevent changing the Super Admin into an organization account.
        super_admin.organization_id = None
        super_admin.email = new_email
        super_admin.password_hash = hash_password(new_password)
        super_admin.is_active = True

        await session.commit()

        print(f"Super Admin updated: {new_email}")

if __name__ == "__main__":
    asyncio.run(update_super_admin())