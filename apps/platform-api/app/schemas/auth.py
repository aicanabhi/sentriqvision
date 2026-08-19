"""
Authentication API schemas.

These schemas define the request and response format for
authentication endpoints without exposing sensitive account data.
"""

from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'