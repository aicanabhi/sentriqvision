from typing import List, Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    tenant_id: str
    org_id: str
    email: str
    full_name: str
    roles: List[str]


class TokenPayload(BaseModel):
    sub: str
    tenant_id: str
    org_id: str
    roles: List[str]
    exp: int
    type: str
