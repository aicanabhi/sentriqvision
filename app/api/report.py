"""
Report API

Handles report generation, listing,
downloading and management.
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_active_user,
    get_current_org_admin,
)

from app.schemas.report import (
    ReportCreate,
    ReportResponse,
)

from app.services.report_service import ReportService


router = APIRouter()


# ==========================================================
# Create Report
# ==========================================================

@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_report(
    report: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Generate a new report.
    """

    service = ReportService(db)

    return await service.create_report(
        report,
        current_user,
    )


# ==========================================================
# List Reports
# ==========================================================

@router.get("")
async def list_reports(
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get all reports.
    """

    service = ReportService(db)

    return await service.list_reports(
        page,
        per_page,
        current_user,
    )


# ==========================================================
# Get Report
# ==========================================================

@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
async def get_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get report details.
    """

    service = ReportService(db)

    return await service.get_report(
        report_id,
        current_user,
    )


# ==========================================================
# Download Report
# ==========================================================

@router.get(
    "/{report_id}/download",
)
async def download_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Download generated report file.
    """

    service = ReportService(db)

    report_file = await service.get_report_file(
        report_id,
        current_user,
    )

    return FileResponse(
        path=report_file.path,
        filename=report_file.name,
        media_type=report_file.content_type,
    )


# ==========================================================
# Delete Report
# ==========================================================

@router.delete(
    "/{report_id}",
)
async def delete_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Delete report.
    """

    service = ReportService(db)

    await service.delete_report(
        report_id,
        current_user,
    )

    return {
        "success": True,
        "message": "Report deleted successfully",
    }


# ==========================================================
# Report Statistics
# ==========================================================

@router.get(
    "/statistics/summary",
)
async def report_statistics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_org_admin),
):
    """
    Report analytics summary.
    """

    service = ReportService(db)

    return await service.report_statistics(
        current_user,
    )


# ==========================================================
# Reports By Type
# ==========================================================

@router.get(
    "/type/{report_type}",
)
async def reports_by_type(
    report_type: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Filter reports by type.

    Examples:
    - security
    - camera
    - parking
    - detection
    """

    service = ReportService(db)

    return await service.get_reports_by_type(
        report_type,
        current_user,
    )