"""
Security Utilities

Handles:

- Password Hashing
- Password Verification
- JWT Access Token
- JWT Refresh Token
- Token Decoding
- API Key Generation
- OTP Generation
- UUID Generation
"""

from datetime import datetime, timedelta, timezone
import secrets
import uuid
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.core.constants import TokenType

# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ==========================================================
# Password
# ==========================================================


def hash_password(password: str) -> str:
    """
    Hash user password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# JWT
# ==========================================================


def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_data: dict | None = None,
) -> str:
    """
    Internal JWT generator.
    """

    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }

    if extra_data:
        payload.update(extra_data)

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


# ==========================================================
# Access Token
# ==========================================================


def create_access_token(
    subject: str,
    extra_data: dict | None = None,
) -> str:

    return _create_token(
        subject=subject,
        token_type=TokenType.ACCESS.value,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        extra_data=extra_data,
    )


# ==========================================================
# Refresh Token
# ==========================================================


def create_refresh_token(
    subject: str,
) -> str:

    return _create_token(
        subject=subject,
        token_type=TokenType.REFRESH.value,
        expires_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )


# ==========================================================
# Password Reset Token
# ==========================================================


def create_password_reset_token(
    subject: str,
) -> str:

    return _create_token(
        subject=subject,
        token_type=TokenType.RESET_PASSWORD.value,
        expires_delta=timedelta(minutes=30),
    )


# ==========================================================
# Verify Token
# ==========================================================


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode JWT token.

    Raises JWTError if invalid.
    """

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )


def verify_token(
    token: str,
    expected_type: str | None = None,
) -> dict[str, Any]:

    payload = decode_token(token)

    if expected_type:

        token_type = payload.get("type")

        if token_type != expected_type:

            raise JWTError("Invalid token type")

    return payload


# ==========================================================
# Helpers
# ==========================================================


def generate_uuid() -> str:
    """
    Generate UUID4.
    """
    return str(uuid.uuid4())