import uuid
from pydantic import BaseModel, Field, ConfigDict

class ZoneCreate(BaseModel):
    site_id: uuid.UUID
    name: str = Field(min_length=1, max_length=255)
    zone_type: str = Field(min_length=1, max_length=100)
    status: str = Field(default="ACTIVE", max_length=50)

class ZoneResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    name: str
    zone_type: str
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )