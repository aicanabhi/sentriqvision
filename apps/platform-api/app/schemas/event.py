import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, ConfigDict

class EventCreate(BaseModel):
    camera_id: uuid.UUID
    zone_id: uuid.UUID
    module_id: uuid.UUID
    event_type: str = Field(min_length=1, max_length=100)
    condition_id: float
    occurred_at: datetime
    event_metadata: dict[str, Any] = Field(default_factory=dict)

class EventResponse(BaseModel):
    id: uuid.UUID
    camera_id: uuid.UUID
    zone_id: uuid.UUID
    module_id: uuid.UUID
    event_type: str
    condition_id: float
    occurred_at: datetime
    event_metadata: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)