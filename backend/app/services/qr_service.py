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
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_qr_boarding_token,
    decode_qr_boarding_token,
)

from app.models.booking import Booking
from app.models.enums import RideStatus
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

    payload = decode_qr_boarding_token(qr_token)

    booking = db.scalar(
        select(Booking).where(
            Booking.ride_id == payload["ride_id"],
            Booking.passenger_id == passenger_id,
        )
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not booked for this ride.",
        )

    ride = booking.ride

    if ride.status != RideStatus.WAITING_FOR_BOARDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride is not waiting for boarding.",
        )

    booking.has_boarded = True

    ride.boarding_verified_at = datetime.now(
        timezone.utc,
    )

    ride.status = RideStatus.IN_PROGRESS

    db.commit()

    db.refresh(ride)

    return ride