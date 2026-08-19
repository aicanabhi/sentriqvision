"""
Authentication service.

Handles credential verification and creation of JWT access tokens.

This layer does not decide organization/resource permissions.
Those checks will be handled by the authorization layer after
authentication succeeds.
"""

from app.security.jwt import create_access_token
from app.security.password import verify_password
from app.repositories.account import AccountRepository

class AuthService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    async def authenticate(self, email: str, password: str) -> str | None:
        """
        Verify account credentials and return a JWT access token.
        Return None when:
        - password is incorrect.
        - account does not exist.
        - account is inactive.
        """
        account = await self.repository.get_by_email(email.lower().strip())

        if account is None:
            return None

        if not account.is_active:
            return None

        if not verify_password(password, account.password_hash):
            return None

        return create_access_token(account.id)
