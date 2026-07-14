
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.application.schemas.common import TimestampsMixin
from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    team_id: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    team_id: Optional[str] = None


class UserResponse(UserBase, TimestampsMixin):
    id: str
    organization_id: str
    team_id: str
