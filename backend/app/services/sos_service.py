"""
==================================================
CommuteShare SOS Service

Backend Internship Project
Bermer Software Private Limited

Handles:
- Create SOS Event
- Retrieve SOS Events
- View SOS History
==================================================
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sos_event import SOSEvent
from app.models.user import User
from app.models.enums import SOSStatus

from app.schemas.misc import SOSCreate


# ==========================================================
# Get SOS By ID
# ==========================================================

def get_sos_by_id(
    db: Session,
    *,
    sos_id: int,
) -> SOSEvent:
    """
    Return an SOS event by ID.
    """

    stmt = select(SOSEvent).where(
        SOSEvent.id == sos_id,
    )

    sos_event = db.scalar(stmt)

    if sos_event is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SOS event not found.",
        )

    return sos_event


# ==========================================================
# User SOS History
# ==========================================================

def get_user_sos_events(
    db: Session,
    *,
    user_id: int,
) -> list[SOSEvent]:
    """
    Return all SOS events
    for a user.
    """

    stmt = (
        select(SOSEvent)
        .where(
            SOSEvent.user_id == user_id,
        )
        .order_by(
            SOSEvent.created_at.desc(),
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Create SOS Event
# ==========================================================

def create_sos_event(
    db: Session,
    *,
    user: User,
    sos_data: SOSCreate,
) -> SOSEvent:
    """
    Create an SOS event.

    Automatically determines the user's active ride
    when possible and prevents duplicate active SOS events.
    """

    # ======================================================
    # Prevent duplicate active SOS events
    # ======================================================

    existing_stmt = (
        select(SOSEvent)
        .where(
            SOSEvent.user_id == user.id,
            SOSEvent.status == SOSStatus.ACTIVE,
        )
        .order_by(SOSEvent.created_at.desc())
    )

    existing_sos = db.scalar(existing_stmt)

    if existing_sos is not None:
        return existing_sos

    # ======================================================
    # Determine active ride automatically
    # ======================================================

    ride_id = sos_data.ride_id

    if ride_id is None:
        from app.models.ride import Ride
        from app.models.booking import Booking
        from app.models.enums import BookingStatus, RideStatus

        # --------------------------------------------------
        # Driver's active ride
        # --------------------------------------------------

        driver_ride_stmt = (
            select(Ride)
            .where(
                Ride.driver_id == user.id,
                Ride.status == RideStatus.IN_PROGRESS,
            )
            .order_by(Ride.created_at.desc())
        )

        active_ride = db.scalar(driver_ride_stmt)

        # --------------------------------------------------
        # Passenger's active ride
        # --------------------------------------------------

        if active_ride is None:
            passenger_ride_stmt = (
                select(Ride)
                .join(
                    Booking,
                    Booking.ride_id == Ride.id,
                )
                .where(
                    Booking.passenger_id == user.id,
                    Booking.status == BookingStatus.CONFIRMED,
                    Ride.status == RideStatus.IN_PROGRESS,
                )
                .order_by(Ride.created_at.desc())
            )

            active_ride = db.scalar(
                passenger_ride_stmt
            )

        if active_ride is not None:
            ride_id = active_ride.id
        if ride_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You do not have an active ride. SOS can only be triggered during an active ride.",
            )

    # ======================================================
    # Create SOS
    # ======================================================

    sos_event = SOSEvent(
        user_id=user.id,
        ride_id=ride_id,
        emergency_type=sos_data.emergency_type,
        description=sos_data.description,
        latitude=sos_data.latitude,
        longitude=sos_data.longitude,
    )

    try:
        db.add(sos_event)

        db.commit()

        db.refresh(sos_event)

        return sos_event

    except Exception:
        db.rollback()
        raise
    