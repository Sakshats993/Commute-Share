"""
==================================================
CommuteShare Admin Service

Backend Internship Project
Bermer Software Private Limited

Handles:
- Dashboard Statistics
- User Management
- Ride Management
- Booking Management
==================================================
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.ride import Ride
from app.models.user import User


# ==========================================================
# Dashboard Statistics
# ==========================================================

def get_dashboard_statistics(
    db: Session,
) -> dict[str, int]:
    """
    Return platform statistics.
    """

    total_users = db.scalar(
        select(func.count()).select_from(User)
    ) or 0

    active_users = db.scalar(
        select(func.count())
        .select_from(User)
        .where(User.is_active.is_(True))
    ) or 0

    total_rides = db.scalar(
        select(func.count()).select_from(Ride)
    ) or 0

    total_bookings = db.scalar(
        select(func.count()).select_from(Booking)
    ) or 0

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_rides": total_rides,
        "total_bookings": total_bookings,
    }


# ==========================================================
# All Users
# ==========================================================

def get_all_users(
    db: Session,
) -> list[User]:
    """
    Return all users.
    """

    stmt = (
        select(User)
        .order_by(User.created_at.desc())
    )

    return list(db.scalars(stmt).all())


# ==========================================================
# All Rides
# ==========================================================

def get_all_rides(
    db: Session,
) -> list[Ride]:
    """
    Return all rides.
    """

    stmt = (
        select(Ride)
        .order_by(Ride.created_at.desc())
    )

    return list(db.scalars(stmt).all())


# ==========================================================
# All Bookings
# ==========================================================

def get_all_bookings(
    db: Session,
) -> list[Booking]:
    """
    Return all bookings.
    """

    stmt = (
        select(Booking)
        .order_by(Booking.created_at.desc())
    )

    return list(db.scalars(stmt).all())


# ==========================================================
# Activate User
# ==========================================================

def activate_user(
    db: Session,
    *,
    user_id: int,
) -> User:
    """
    Activate a user account.
    """

    stmt = select(User).where(User.id == user_id)

    user = db.scalar(stmt)

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.is_active = True

    try:

        db.commit()

        db.refresh(user)

    except Exception:

        db.rollback()

        raise

    return user


# ==========================================================
# Deactivate User
# ==========================================================

def deactivate_user(
    db: Session,
    *,
    user_id: int,
) -> User:
    """
    Deactivate a user account.
    """

    stmt = select(User).where(User.id == user_id)

    user = db.scalar(stmt)

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.is_active = False

    try:

        db.commit()

        db.refresh(user)

    except Exception:

        db.rollback()

        raise

    return user