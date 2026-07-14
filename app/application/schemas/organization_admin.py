
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.application.schemas.common import TimestampsMixin


class OrganizationAdminBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = None


class OrganizationAdminCreate(OrganizationAdminBase):
    password: str = Field(..., min_length=8)


class OrganizationAdminResponse(OrganizationAdminBase, TimestampsMixin):
    id: str
    organization_id: str
