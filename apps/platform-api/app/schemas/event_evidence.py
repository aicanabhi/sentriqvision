import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class EventEvidenceCreate(BaseModel):
    event_id: uuid.UUID
    evidence_type: str = Field(min_length=1, max_length=50)
    storage_key: str = Field(min_length=1, max_length=1000)
    mime_type: str = Field(min_length=1, max_length=100)
    captured_at: datetime

class EventEvidenceResponse(BaseModel):
    id: uuid.UUID
    event_id: uuid.UUID
    evidence_type: str
    storage_key: str
    mime_type: str
    captured_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)