import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class OrganizationCreate(BaseModel):
    name: str
    status: str = "ACTIVE"

class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)