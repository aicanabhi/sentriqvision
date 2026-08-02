"""JWT token creation and validation."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from uuid import uuid4

from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import (
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_OTP,
    TOKEN_TYPE_REFRESH,
    TOKEN_TYPE_RESET,
    TOKEN_TYPE_VERIFY,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_token(
    subject: str,
    token_type: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    if expires_delta is None:
        if token_type == TOKEN_TYPE_ACCESS:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        elif token_type == TOKEN_TYPE_REFRESH:
            expires_delta = timedelta(days=settings.refresh_token_expire_days)
        elif token_type == TOKEN_TYPE_RESET:
            expires_delta = timedelta(minutes=settings.password_reset_token_expire_minutes)
        elif token_type == TOKEN_TYPE_OTP:
            expires_delta = timedelta(minutes=settings.otp_expire_minutes)
        else:
            expires_delta = timedelta(minutes=30)

    expire = _utcnow() + expires_delta
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "exp": expire,
        "iat": _utcnow(),
        "jti": str(uuid4()),
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def verify_token(token: str, expected_type: str) -> dict[str, Any]:
    try:
        payload = decode_token(token)
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc

    if payload.get("type") != expected_type:
        raise ValueError(f"Invalid token type. Expected {expected_type}")

    return payload


def create_access_token(subject: str, **extra_claims: Any) -> str:
    return create_token(subject, TOKEN_TYPE_ACCESS, extra_claims=extra_claims)


def create_refresh_token(subject: str, **extra_claims: Any) -> str:
    return create_token(subject, TOKEN_TYPE_REFRESH, extra_claims=extra_claims)


def create_reset_token(subject: str) -> str:
    return create_token(subject, TOKEN_TYPE_RESET)


def create_verify_token(subject: str) -> str:
    return create_token(subject, TOKEN_TYPE_VERIFY, expires_delta=timedelta(hours=24))


def create_otp_token(subject: str, otp: str) -> str:
    return create_token(subject, TOKEN_TYPE_OTP, extra_claims={"otp": otp})
