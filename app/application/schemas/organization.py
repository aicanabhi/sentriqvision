
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.application.schemas.common import TimestampsMixin
from enum import Enum


class OrganizationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: OrganizationStatus = OrganizationStatus.ACTIVE


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class OrganizationResponse(OrganizationBase, TimestampsMixin):
    id: str
