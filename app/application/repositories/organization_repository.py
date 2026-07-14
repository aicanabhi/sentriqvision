
from app.application.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "organizations")
