"""
Create the initial SentriqVision Super Admin account.

This is intended for initial platform provisioning only.
A Super Admin:
    - has no organization_id
    - has platform-wide administrative access
    - is created outside the normal organization account flow
"""

import asyncio
import getpass
from sqlalchemy import select
from app.auth import AccountRole
from app.database.connection import AsyncSessionLocal
from app.models.account import Account
from app.security.password import hash_password

async def create_super_admin() -> None:
    email = input("Super Admin Email: ").strip().lower()
    password = getpass.getpass("Super Admin Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")

    if password != confirm_password:
        raise Exception("Passwords don't match")

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Account).where(Account.role == AccountRole.SUPER_ADMIN.value)
        )

        existing = result.scalar_one_or_none()

        if existing is not None:
            raise ValueError("A Super Admin account already exists")

        account = Account(
            email=email,
            password_hash=hash_password(password),
            role=AccountRole.SUPER_ADMIN.value,
            organization_id=None,
            is_active=True,
        )

        session.add(account)
        await session.commit()

        print(f"Super Admin created: {email}")

if __name__ == "__main__":
    asyncio.run(create_super_admin())