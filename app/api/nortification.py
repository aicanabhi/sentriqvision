"""
Notification API

Handles:
- Create notifications
- List notifications
- Read notifications
- Delete notifications
- User notification management
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_active_user,
    pagination_params,
)

from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)

from app.services.notification_service import NotificationService


router = APIRouter()


# ==========================================================
# Create Notification
# ==========================================================


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_notification(
    notification: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create new notification.
    """

    service = NotificationService(db)

    return await service.create_notification(
        notification
    )


# ==========================================================
# Get My Notifications
# ==========================================================


@router.get(
    "",
)
async def get_notifications(
    pagination=Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get logged-in user notifications.
    """

    service = NotificationService(db)

    return await service.get_user_notifications(
        user_id=current_user["id"],
        page=pagination["page"],
        per_page=pagination["per_page"],
    )


# ==========================================================
# Get Single Notification
# ==========================================================


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
async def get_notification(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get notification details.
    """

    service = NotificationService(db)

    return await service.get_notification(
        notification_id
    )


# ==========================================================
# Mark Notification Read
# ==========================================================


@router.patch(
    "/{notification_id}/read",
)
async def mark_notification_read(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Mark notification as read.
    """

    service = NotificationService(db)

    return await service.mark_as_read(
        notification_id
    )


# ==========================================================
# Mark All Notifications Read
# ==========================================================


@router.patch(
    "/read-all",
)
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Mark all user notifications as read.
    """

    service = NotificationService(db)

    return await service.mark_all_as_read(
        current_user["id"]
    )


# ==========================================================
# Update Notification
# ==========================================================


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
async def update_notification(
    notification_id: UUID,
    data: NotificationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update notification.
    """

    service = NotificationService(db)

    return await service.update_notification(
        notification_id,
        data,
    )


# ==========================================================
# Delete Notification
# ==========================================================


@router.delete(
    "/{notification_id}",
)
async def delete_notification(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Delete notification.
    """

    service = NotificationService(db)

    await service.delete_notification(
        notification_id
    )

    return {
        "success": True,
        "message": "Notification deleted successfully",
    }