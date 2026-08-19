"""
Authorization dependencies.

Resource-level authorization for sites, cameras, events, and
evidence will be enforced separately.
"""

from collections.abc import Callable
from fastapi import Depends, HTTPException, status
from app.auth import AccountRole
from app.models.account import Account
from app.security.dependencies import get_current_account

def require_roles(
        *allowed_roles: AccountRole,
) -> Callable:
    """
    Create a FastAPI dependency that restricts an endpoint
    to the supplied account roles.
    """

    async def role_checker(
            account: Account = Depends(get_current_account),
    ) -> Account:

        if account.role not in {
            role.value for role in allowed_roles
        }:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return account
    return role_checker