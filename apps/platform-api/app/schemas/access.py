"""
API schemas for organization resource access management.
"""
from uuid import UUID
from pydantic import BaseModel

class GrantSiteAccessRequest(BaseModel):
    account_id: UUID
    site_id: UUID

class GrantCameraAccessRequest(BaseModel):
    account_id: UUID
    camera_id: UUID

class AccessResponse(BaseModel):
    account_id: UUID
    resource_id: UUID
    resource_type: str