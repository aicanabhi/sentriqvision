
from app.application.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "teams")
