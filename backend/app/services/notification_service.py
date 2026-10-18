"""
==================================================
CommuteShare Notification Service

Backend Internship Project
Bermer Software Private Limited

Handles creation and management of user
notifications.

Examples:
- Ride Booked
- Ride Cancelled
- Waitlist Promotion
- SOS Alert
- Rating Received
==================================================
"""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import NotificationType
from app.models.notification import Notification


def create_notification(
    db: Session,
    *,
    user_id: int,
    title: str,
    message: str,
    notification_type: NotificationType,
    commit: bool = True,
) -> Notification:
    """
    Create a notification for a user.
    """

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type,
    )

    try:
        db.add(notification)
        if commit:
            db.commit()
            db.refresh(notification)
        else:
            db.flush()

    except Exception:
        db.rollback()
        raise

    return notification


def get_notifications(
    db: Session,
    *,
    user_id: int,
) -> List[Notification]:
    """
    Return all notifications for a user.
    """

    stmt = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )

    return list(db.scalars(stmt).all())


def get_unread_notifications(
    db: Session,
    *,
    user_id: int,
) -> List[Notification]:
    """
    Return unread notifications for a user.
    """

    stmt = (
        select(Notification)
        .where(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
        .order_by(Notification.created_at.desc())
    )

    return list(db.scalars(stmt).all())


def mark_as_read(
    db: Session,
    *,
    notification: Notification,
) -> Notification:
    """
    Mark a notification as read.
    """

    notification.is_read = True

    try:
        db.commit()
        db.refresh(notification)

    except Exception:
        db.rollback()
        raise

    return notification


def mark_all_as_read(
    db: Session,
    *,
    user_id: int,
) -> int:
    """
    Mark all notifications as read.

    Returns:
        Number of notifications updated.
    """

    stmt = (
        select(Notification)
        .where(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
    )

    notifications = list(db.scalars(stmt).all())

    if not notifications:
        return 0

    for notification in notifications:
        notification.is_read = True

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise

    return len(notifications)


def delete_notification(
    db: Session,
    *,
    notification: Notification,
) -> None:
    """
    Permanently delete a notification.
    """

    try:
        db.delete(notification)
        db.commit()

    except Exception:
        db.rollback()
        raise
