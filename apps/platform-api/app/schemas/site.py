import uuid
from pydantic import BaseModel, Field, ConfigDict

class SiteCreate(BaseModel):
    organization_id: uuid.UUID
    name: str = Field(min_length=1, max_length=255)
    timezone: str = Field(default="UTC", max_length=100)
    status: str = Field(default="active", max_length=50)

class SiteResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    timezone: str
    status: str

    model_config = ConfigDict(from_attributes=True)