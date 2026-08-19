import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.auth import AccountRole

class AccountCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: AccountRole
    organization_id: uuid.UUID | None = None

class AccountResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID | None
    email: EmailStr
    role: AccountRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)