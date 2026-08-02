"""
Parking Service
"""

from sqlalchemy.ext.asyncio import AsyncSession


class ParkingService:
    def __init__(self, db: AsyncSession):
        self.db = db
