import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class OrganizationCreate(BaseModel):
    name: str
    slug: str


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TenantCreate(BaseModel):
    organization_id: uuid.UUID
    name: str
    code: str
    config: Optional[dict] = {}


class TenantResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    code: str
    config: dict
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
