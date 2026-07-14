
from app.application.repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "refresh_tokens")
