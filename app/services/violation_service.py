"""
Violation Service
"""

from sqlalchemy.ext.asyncio import AsyncSession


class ViolationService:
    def __init__(self, db: AsyncSession):
        self.db = db
