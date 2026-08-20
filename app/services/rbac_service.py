import uuid
from typing import List, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.exceptions import PlatformException
from app.core.security import decode_access_token
from app.models.user import User

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise PlatformException(
            code="UNAUTHORIZED",
            message="Authorization bearer token required",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Sub missing")
    except Exception:
        raise PlatformException(
            code="INVALID_TOKEN",
            message="Could not validate credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    query = (
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == uuid.UUID(user_id))
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise PlatformException(
            code="USER_NOT_FOUND",
            message="User associated with token not found or inactive",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return user


def require_roles(allowed_roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.is_superuser:
            return current_user

        user_role_names = [r.name for r in current_user.roles]
        if not any(r in allowed_roles for r in user_role_names):
            raise PlatformException(
                code="FORBIDDEN",
                message=f"Action requires one of roles: {allowed_roles}",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return current_user

    return role_checker
