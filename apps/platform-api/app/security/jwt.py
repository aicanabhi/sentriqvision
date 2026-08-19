"""
JWT authentication utilities.

This module is responsible only for creating and decoding JWT access
tokens.

The token identifies the authenticated account. Authorization decisions
are still enforced by the application using the account's current
database state.
"""

import uuid
from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

ALGORITHM = 'HS256'

def create_access_token(account_id: uuid.UUID,) -> str:
    """
    Create a JWT access token for an authenticated account.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(account_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )

def decode_access_token(token: str) -> uuid.UUID:
    """
    Decode and validate a JWT access token.

    Returns the account UUID stored in the 'sub' claim.
    """
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
    subject = payload.get("sub")

    if not subject:
        raise ValueError("Token does not contain an account ID")

    try:
        return uuid.UUID(subject)
    except ValueError as exc:
        raise ValueError("Invalid account ID in token") from exc