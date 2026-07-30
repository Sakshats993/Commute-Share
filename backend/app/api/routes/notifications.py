"""
==================================================
CommuteShare Notification Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- View Notifications
- View Unread Notifications
- Mark Notification as Read
- Mark All Notifications as Read
==================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.models.notification import Notification
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_active_user,
    get_db,
)

from app.models.user import User

from app.schemas.misc import NotificationResponse



from app.services.notification_service import (
    get_notifications,
    get_unread_notifications,
    mark_all_as_read,
    mark_as_read,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# ==========================================================
# All Notifications
# ==========================================================

@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def get_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return all notifications for the current user.
    """

    return get_notifications(
        db=db,
        user_id=current_user.id,
    )


# ==========================================================
# Unread Notifications
# ==========================================================

@router.get(
    "/unread",
    response_model=list[NotificationResponse],
)
def get_unread(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return unread notifications.
    """

    return get_unread_notifications(
        db=db,
        user_id=current_user.id,
    )


# ==========================================================
# Mark Notification as Read
# ==========================================================
@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    notification = db.scalar(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    return mark_as_read(
        db=db,
        notification=notification,
    )

# ==========================================================
# Mark All Notifications as Read
# ==========================================================

@router.patch(
    "/read-all",
)
def mark_everything_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Mark all notifications as read.
    """

    mark_all_as_read(
        db=db,
        user_id=current_user.id,
    )

    return {
        "message": "All notifications marked as read."
    }