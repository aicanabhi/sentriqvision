"""
Account service.

Contains business rules for creating and managing authentication
accounts. Persistence is delegated to AccountRepository.

Authorization rules:
    SUPER_ADMIN:
        organization_id must be NULL.

    ADMIN / OPERATOR / AUTHORIZED_VIEWER:
        organization_id is required.
"""

import uuid
from app.auth import AccountRole
from app.models.account import Account
from app.repositories.account import AccountRepository
from app.security.password import hash_password

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    async def get_by_id(self, account_id: uuid.UUID) -> Account | None:
        return await self.repository.get_by_id(account_id)

    async def get_by_email(self, email: str) -> Account | None:
        return await self.repository.get_by_email(email.lower().strip())

    async def get_all(self) -> list[Account]:
        return await self.repository.get_all()

    async def create(
            self,
            email: str,
            password: str,
            role: AccountRole,
            organization_id: uuid.UUID | None = None,
    ) -> Account:

        email = email.lower().strip()
        existing = await self.repository.get_by_email(email)

        if existing is not None:
            raise ValueError(f"Account with this email already exists")

        if role == AccountRole.SUPER_ADMIN:
            if organization_id is not None:
                raise ValueError("SUPER_ADMIN cannot belong to an organization")

        else:
            if organization_id is None:
                raise ValueError("Organization required for this role")

        password_hash = hash_password(password)

        return await self.repository.create(
            email=email,
            password_hash=password_hash,
            role=role.value,
            organization_id=organization_id
        )