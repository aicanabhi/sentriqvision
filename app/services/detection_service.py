"""
Detection Service

Business logic for AI detection events.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.detection import Detection
from app.schemas.detection import DetectionCreate


class DetectionService:
    """
    Handles detection operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db


    async def create_detection(
        self,
        data: DetectionCreate,
    ):

        detection = Detection(
            **data.model_dump()
        )

        self.db.add(detection)

        await self.db.commit()
        await self.db.refresh(detection)

        return detection


    async def get_detection(
        self,
        detection_id: UUID,
    ):

        result = await self.db.get(
            Detection,
            detection_id
        )

        return result


    async def list_detections(
        self,
        skip: int = 0,
        limit: int = 20,
    ):

        result = await self.db.execute(
            select(Detection)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()