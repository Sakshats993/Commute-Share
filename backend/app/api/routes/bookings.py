"""
==================================================
CommuteShare Booking Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- Book Ride
- Cancel Booking
- View User Bookings
- View Ride Bookings
- Booking Statistics
==================================================
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_active_user,
    get_db,
)

from app.models.user import User

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)

from app.services.booking_service import (
    book_ride,
    cancel_booking,
    get_booking_by_id,
    get_booking_statistics,
    get_ride_bookings,
    get_user_bookings,
)

from app.services.ride_service import (
    get_ride_by_id,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)
# ==========================================================
# Book Ride
# ==========================================================

@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking_route(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Book a ride.
    """

    ride = get_ride_by_id(
        db=db,
        ride_id=booking_data.ride_id,
    )

    return book_ride(
        db=db,
        ride=ride,
        passenger=current_user,
    )
  
# ==========================================================
# Ride Bookings
# ==========================================================

@router.get(
    "/ride/{ride_id}",
    response_model=list[BookingResponse],
)
def ride_bookings(
    ride_id: int,
    db: Session = Depends(get_db),
):
    """
    Return bookings for a ride.
    """

    return get_ride_bookings(
        db=db,
        ride_id=ride_id,
    )
# ==========================================================
# Booking Statistics
# ==========================================================

@router.get(
    "/me/statistics",
)
def booking_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return booking statistics.
    """

    return get_booking_statistics(
        db=db,
        passenger_id=current_user.id,
    )
# ==========================================================
# My Bookings
# ==========================================================

@router.get(
    "/me",
    response_model=list[BookingResponse],
)
def my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return all bookings for the current user.
    """

    return get_user_bookings(
        db=db,
        user_id=current_user.id,
    )

# ==========================================================
# Cancel Booking
# ==========================================================

@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_booking_route(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Cancel a booking.
    """

    booking = get_booking_by_id(
        db=db,
        booking_id=booking_id,
    )

    if booking.passenger_id != current_user.id:

        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot cancel this booking.",
        )

    cancel_booking(
        db=db,
        booking=booking,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )