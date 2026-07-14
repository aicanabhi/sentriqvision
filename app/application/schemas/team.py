
from pydantic import BaseModel, Field
from typing import Optional
from app.application.schemas.common import TimestampsMixin


class TeamBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TeamResponse(TeamBase, TimestampsMixin):
    id: str
    organization_id: str
