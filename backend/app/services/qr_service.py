"""
==================================================
CommuteShare QR Service

Backend Internship Project
Bermer Software Private Limited

Handles:

- QR Generation
- QR Verification
- Boarding Verification
==================================================
"""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_qr_boarding_token,
    decode_qr_boarding_token,
)

from app.models.booking import Booking
from app.models.enums import BookingStatus, RideStatus
from app.models.ride import Ride


# ======================================================
# Generate QR
# ======================================================

def generate_boarding_qr(
    *,
    ride: Ride,
) -> str:
    """
    Generate a signed QR token for boarding.
    """

    return create_qr_boarding_token(
        ride_id=ride.id,
        driver_id=ride.driver_id,
    )


# ======================================================
# Verify QR
# ======================================================

def verify_boarding_qr(
    *,
    db: Session,
    qr_token: str,
    passenger_id: int,
) -> Ride:
    """
    Verify a boarding QR token.
    """

    try:
        payload = decode_qr_boarding_token(qr_token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired boarding QR code.",
        ) from exc

    ride = db.scalar(
        select(Ride)
        .where(Ride.id == payload.get("ride_id"))
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if ride is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found.",
        )

    booking = db.scalar(
        select(Booking)
        .where(
            Booking.ride_id == payload["ride_id"],
            Booking.passenger_id == passenger_id,
        )
        .with_for_update()
        .execution_options(populate_existing=True)
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not booked for this ride.",
        )

    if ride.driver_id != payload.get("driver_id"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Boarding QR code does not match this ride.",
        )

    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only confirmed passengers can board this ride.",
        )

    if booking.has_boarded:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This booking has already been checked in.",
        )

    if ride.status not in (
        RideStatus.WAITING_FOR_BOARDING,
        RideStatus.IN_PROGRESS,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride is not waiting for boarding.",
        )

    try:
        booking.has_boarded = True
        if ride.boarding_verified_at is None:
            ride.boarding_verified_at = datetime.now(timezone.utc)
        ride.status = RideStatus.IN_PROGRESS
        db.commit()
        db.refresh(ride)
    except Exception:
        db.rollback()
        raise

    return ride
