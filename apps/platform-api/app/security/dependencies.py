"""
Authentication dependencies.

Provides FastAPI dependencies for extracting the authenticated
Account from a JWT Bearer token.

Authentication only happens here.
Role and resource-level authorization will be implemented separately.
"""

import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.repositories.account import AccountRepository
from app.security.jwt import decode_access_token

bearer_scheme = HTTPBearer()

async def get_current_account(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: AsyncSession = Depends(get_db)
):
    """
    Return the currently authenticated account.

    Raises:
    401: Missing, invalid, expired, or inactive authentication.
    """
    try:
        account_id: uuid.UUID = decode_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    repository = AccountRepository(session)

    account = await repository.get_by_id(account_id)

    if account is None or not account.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is not active or does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return account