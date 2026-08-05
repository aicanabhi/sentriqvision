"""
Vehicle Service
"""

from sqlalchemy.ext.asyncio import AsyncSession


class VehicleService:
    def __init__(self, db: AsyncSession):
        self.db = db
