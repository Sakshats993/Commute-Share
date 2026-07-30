"""
==================================================
CommuteShare Admin Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- User Management
- Ride Management
- Booking Management
- Dashboard Statistics
==================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import (
    get_db,
    require_admin,
)

from app.models.user import User

from app.services.admin_service import (
    get_dashboard_statistics,
    get_all_users,
    get_all_rides,
    get_all_bookings,
    deactivate_user,
    activate_user,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)
# ==========================================================
# Dashboard Statistics
# ==========================================================

@router.get(
    "/dashboard",
)
def dashboard(
    db: Session = Depends(get_db),
):
    """
    Return admin dashboard statistics.
    """

    return get_dashboard_statistics(
        db=db,
    )
# ==========================================================
# Users
# ==========================================================

@router.get(
    "/users",
)
def users(
    db: Session = Depends(get_db),
):
    """
    Return all users.
    """

    return get_all_users(
        db=db,
    )
# ==========================================================
# Activate User
# ==========================================================

@router.patch(
    "/users/{user_id}/activate",
)
def activate(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Activate a user account.
    """

    return activate_user(
        db=db,
        user_id=user_id,
    )
# ==========================================================
# Deactivate User
# ==========================================================

@router.patch(
    "/users/{user_id}/deactivate",
)
def deactivate(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Deactivate a user account.
    """

    return deactivate_user(
        db=db,
        user_id=user_id,
    )   
# ==========================================================
# Rides
# ==========================================================

@router.get(
    "/rides",
)
def rides(
    db: Session = Depends(get_db),
):
    """
    Return all rides.
    """

    return get_all_rides(
        db=db,
    )
# ==========================================================
# Bookings
# ==========================================================

@router.get(
    "/bookings",
)
def bookings(
    db: Session = Depends(get_db),
):
    """
    Return all bookings.
    """

    return get_all_bookings(
        db=db,
    )