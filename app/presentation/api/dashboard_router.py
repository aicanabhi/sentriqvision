from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.infrastructure.database.mongodb import get_database
from app.application.services.dashboard_service import DashboardService
from app.application.schemas.dashboard import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Dashboard Summary"
)
async def get_dashboard(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    service = DashboardService(db)
    return await service.get_dashboard()