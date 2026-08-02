"""
Organization Service
"""

from sqlalchemy.orm import Session

from app.models.organization import Organization


class OrganizationService:
    """
    Handles organization related operations.
    """

    def __init__(self, db: Session):
        self.db = db


    def get_by_id(self, organization_id: str):
        return (
            self.db.query(Organization)
            .filter(
                Organization.id == organization_id
            )
            .first()
        )


    def create(self, data: dict):
        organization = Organization(**data)

        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization


    def delete(self, organization_id: str):
        organization = self.get_by_id(organization_id)

        if organization:
            self.db.delete(organization)
            self.db.commit()

        return organization