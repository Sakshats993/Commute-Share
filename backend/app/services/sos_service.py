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
from app.models.enums import BookingStatus, NotificationType, RideStatus, SOSStatus, UserRole
from app.models.booking import Booking
from app.models.ride import Ride

from app.schemas.misc import SOSCreate
from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification


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
    active_ride_statuses = (RideStatus.WAITING_FOR_BOARDING, RideStatus.IN_PROGRESS)

    if ride_id is None:
        # --------------------------------------------------
        # Driver's active ride
        # --------------------------------------------------

        driver_ride_stmt = (
            select(Ride)
            .where(
                Ride.driver_id == user.id,
                Ride.status.in_(active_ride_statuses),
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
                    Ride.status.in_(active_ride_statuses),
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
    else:
        ride = db.scalar(select(Ride).where(Ride.id == ride_id))
        is_driver_on_ride = bool(
            ride
            and ride.driver_id == user.id
            and ride.status in active_ride_statuses
        )
        is_confirmed_passenger = bool(
            ride
            and ride.status in active_ride_statuses
            and db.scalar(
                select(Booking.id).where(
                    Booking.ride_id == ride.id,
                    Booking.passenger_id == user.id,
                    Booking.status == BookingStatus.CONFIRMED,
                )
            )
        )
        if not (is_driver_on_ride or is_confirmed_passenger):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="SOS can only be linked to your own active ride.",
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
        db.flush()
        admin_ids = db.scalars(
            select(User.id).where(
                User.role == UserRole.ADMIN,
                User.is_active.is_(True),
            )
        ).all()
        for admin_id in admin_ids:
            create_notification(
                db,
                user_id=admin_id,
                title="New SOS safety event",
                message=f"A user triggered SOS event #{sos_event.id}. Review it in admin safety triage.",
                notification_type=NotificationType.SOS_TRIGGERED,
                commit=False,
            )
        create_audit_log(
            db=db,
            action="SOS_TRIGGERED",
            resource="SOSEvent",
            user_id=user.id,
            description=f"SOS event #{sos_event.id} recorded.",
            commit=False,
        )
        db.commit()
        db.refresh(sos_event)

        return sos_event

    except Exception:
        db.rollback()
        raise


def list_sos_events(db: Session, status_filter: SOSStatus | None = None) -> list[SOSEvent]:
    stmt = select(SOSEvent).order_by(SOSEvent.created_at.desc())
    if status_filter is not None:
        stmt = stmt.where(SOSEvent.status == status_filter)
    return list(db.scalars(stmt).all())


def update_sos_status(
    db: Session,
    *,
    sos_id: int,
    admin: User,
    target_status: SOSStatus,
) -> SOSEvent:
    event = get_sos_by_id(db, sos_id=sos_id)
    valid_transition = (
        event.status == SOSStatus.ACTIVE
        and target_status in (SOSStatus.ACKNOWLEDGED, SOSStatus.RESOLVED)
    ) or (
        event.status == SOSStatus.ACKNOWLEDGED
        and target_status == SOSStatus.RESOLVED
    )
    if not valid_transition:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This SOS event has already been handled.",
        )
    try:
        event.status = target_status
        create_audit_log(
            db=db,
            action=f"SOS_{target_status.value.upper()}",
            resource="SOSEvent",
            user_id=admin.id,
            description=f"Admin updated SOS event #{event.id} to {target_status.value}.",
            commit=False,
        )
        create_notification(
            db,
            user_id=event.user_id,
            title="SOS event status updated",
            message=f"Your recorded SOS event #{event.id} is now {target_status.value}.",
            notification_type=NotificationType.SOS_TRIGGERED,
            commit=False,
        )
        db.commit()
        db.refresh(event)
        return event
    except Exception:
        db.rollback()
        raise

