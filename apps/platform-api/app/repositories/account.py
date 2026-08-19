import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account

class AccountRepository:
    """
    Database access layer for authentication accounts.

    This repository is responsible only for persistence and querying.
    Authentication and authorization rules belong in the service layer.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            account_id: uuid.UUID,
    ) -> Account | None:
        result = await self.session.execute(select(Account).where(Account.id == account_id))
        return result.scalar_one_or_none()

    async def get_by_email(
            self,
            email: str,
    ) -> Account | None:
        result = await self.session.execute(select(Account).where(Account.email == email))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Account]:
        result = await self.session.execute(select(Account).order_by(Account.created_at.desc()))
        return list(result.scalars().all())

    async def create(
            self,
            email: str,
            password_hash: str,
            role: str,
            organization_id: uuid.UUID | None = None,
    ) -> Account:
        account = Account(
            email=email,
            password_hash=password_hash,
            role=role,
            organization_id=organization_id,
        )
        self.session.add(account)
        await self.session.flush()

        return account