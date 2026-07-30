"""
==================================================
CommuteShare Booking Service

Backend Internship Project
Bermer Software Private Limited

Handles all ride booking operations.

Features:
- Ride Booking
- Ride Cancellation
- Waitlist Management
- Seat Management
- Booking Validation
- Audit Logging
- Notifications
==================================================
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.booking import Booking
from app.models.enums import BookingStatus, RideStatus
from app.models.ride import Ride
from app.models.user import User
from app.models.waitlist import Waitlist

from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification

from app.models.enums import NotificationType

from datetime import datetime, timezone 

# ==========================================================
# Booking Lookup
# ==========================================================

def get_booking_by_id(
    db: Session,
    booking_id: int,
) -> Booking:
    """
    Return a booking by ID.

    Raises:
        HTTPException(404)
        if booking does not exist.
    """

    stmt = (
        select(Booking)
        .where(Booking.id == booking_id)
    )

    booking = db.scalar(stmt)

    if booking is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    return booking


# ==========================================================
# User Bookings
# ==========================================================

def get_user_bookings(
    db: Session,
    *,
    user_id: int,
) -> list[Booking]:
    """
    Return all bookings
    belonging to a passenger.
    """

    stmt = (
        select(Booking)
        .where(
            Booking.passenger_id == user_id
        )
        .order_by(
            Booking.created_at.desc()
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Ride Bookings
# ==========================================================

def get_ride_bookings(
    db: Session,
    *,
    ride_id: int,
) -> list[Booking]:
    """
    Return all bookings
    for a ride.
    """

    stmt = (
        select(Booking)
        .where(
            Booking.ride_id == ride_id
        )
        .order_by(
            Booking.created_at
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Duplicate Booking Check
# ==========================================================

def check_duplicate_booking(
    db: Session,
    *,
    ride_id: int,
    passenger_id: int,
) -> None:
    """
    Prevent duplicate bookings.
    """

    stmt = (
        select(Booking)
        .where(
            Booking.ride_id == ride_id,
            Booking.passenger_id == passenger_id,
            Booking.status != BookingStatus.CANCELLED,
        )
    )

    existing = db.scalar(stmt)

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this ride.",
        )


# ==========================================================
# Driver Booking Validation
# ==========================================================

def check_driver_booking_own_ride(
    *,
    ride: Ride,
    passenger: User,
) -> None:
    """
    Drivers cannot book
    their own rides.
    """

    if ride.driver_id == passenger.id:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Drivers cannot book their own rides.",
        )


# ==========================================================
# Ride Availability
# ==========================================================

def check_ride_availability(
    ride: Ride,
) -> None:
    """
    Ensure ride is available
    for booking.
    """

    if ride.status != RideStatus.SCHEDULED:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride is not available.",
        )


# ==========================================================
# Seat Availability
# ==========================================================

def check_available_seats(
    ride: Ride,
) -> bool:
    """
    Returns True if seats
    are available.
    """

    return ride.available_seats > 0


# ==========================================================
# Seat Management
# ==========================================================

def decrease_available_seats(
    ride: Ride,
) -> None:
    """
    Reduce available seats
    by one.
    """

    if ride.available_seats <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No seats available.",
        )

    ride.available_seats -= 1


def increase_available_seats(
    ride: Ride,
) -> None:
    """
    Increase available seats.
    """

    if ride.available_seats < ride.total_seats:

        ride.available_seats += 1


# ==========================================================
# Waitlist Lookup
# ==========================================================

def get_waitlist(
    db: Session,
    *,
    ride_id: int,
) -> list[Waitlist]:
    """
    Return waitlist ordered
    by queue position.
    """

    stmt = (
        select(Waitlist)
        .where(
            Waitlist.ride_id == ride_id
        )
        .order_by(
            Waitlist.queue_position
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Next Queue Position
# ==========================================================

def get_next_queue_position(
    db: Session,
    *,
    ride_id: int,
) -> int:
    """
    Return the next available
    queue position.
    """

    waitlist = get_waitlist(
        db,
        ride_id=ride_id,
    )

    if not waitlist:
        return 1

    return waitlist[-1].queue_position + 1

# ==========================================================
# Booking Creation
# ==========================================================

def create_booking(
    db: Session,
    *,
    ride: Ride,
    passenger: User,
) -> Booking:
    """
    Create a confirmed booking.

    Assumes all validations
    have already passed.
    """

    booking = Booking(
        ride_id=ride.id,
        passenger_id=passenger.id,
        status=BookingStatus.CONFIRMED,
    )

    decrease_available_seats(ride)

    try:

        db.add(booking)

        db.commit()

        db.refresh(booking)

        db.refresh(ride)

        create_notification(
            db=db,
            user_id=passenger.id,
            title="Ride Booked",
            message="Your booking has been confirmed.",
            notification_type=NotificationType.RIDE_BOOKED,
        )

        create_notification(
            db=db,
            user_id=ride.driver_id,
            title="New Passenger",
            message=f"{passenger.full_name} booked your ride.",
            notification_type=NotificationType.RIDE_BOOKED,
        )

        create_audit_log(
            db=db,
            action="BOOK",
            resource="Booking",
            user_id=passenger.id,
            description=f"Booking #{booking.id} created.",
        )

    except Exception:

        db.rollback()

        raise

    return booking


# ==========================================================
# Join Waitlist
# ==========================================================
def join_waitlist(
    db: Session,
    *,
    ride: Ride,
    passenger: User,
) -> Waitlist:

    if is_passenger_in_waitlist(
        db=db,
        ride_id=ride.id,
        passenger_id=passenger.id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passenger already in waitlist.",
        )

    waitlist_entry = Waitlist(

        ride_id=ride.id,

        passenger_id=passenger.id,

        queue_position=get_next_queue_position(

            db,

            ride_id=ride.id,
        ),
    )

    try:

        db.add(waitlist_entry)

        db.commit()

        db.refresh(waitlist_entry)

        create_notification(

            db=db,

            user_id=passenger.id,

            title="Added to Waitlist",

            message="Ride is currently full. You have been added to the waitlist.",

            notification_type=NotificationType.WAITLIST_JOINED,

        )   

        create_audit_log(

            db=db,

            action="WAITLIST",

            resource="Ride",

            user_id=passenger.id,

            description=f"Joined waitlist for ride {ride.id}.",
        )

    except Exception:

        db.rollback()

        raise

    return waitlist_entry


# ==========================================================
# Book Ride
# ==========================================================

def book_ride(
    db: Session,
    *,
    ride: Ride,
    passenger: User,
) -> Booking | Waitlist:
    """
    Book a ride.

    If no seats are available,
    passenger is automatically
    added to the waitlist.
    """

    check_ride_availability(ride)

    check_driver_booking_own_ride(

        ride=ride,

        passenger=passenger,
    )

    check_duplicate_booking(

        db=db,

        ride_id=ride.id,

        passenger_id=passenger.id,
    )

    if not check_available_seats(ride):

        return join_waitlist(

            db=db,

            ride=ride,

            passenger=passenger,
        )

    return create_booking(

        db=db,

        ride=ride,

        passenger=passenger,
    )
    # ==========================================================
# Recalculate Waitlist Positions
# ==========================================================

def recalculate_waitlist_positions(
    db: Session,
    *,
    ride_id: int,
) -> None:
    """
    Recalculate queue positions after
    a passenger leaves the waitlist.
    """

    waitlist = get_waitlist(
        db,
        ride_id=ride_id,
    )

    for index, entry in enumerate(waitlist, start=1):
        entry.queue_position = index

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise


# ==========================================================
# Promote Waitlist
# ==========================================================

def promote_waitlist(
    db: Session,
    *,
    ride: Ride,
) -> Booking | None:
    """
    Promote the first passenger
    from the waitlist.
    """

    waitlist = get_waitlist(
        db,
        ride_id=ride.id,
    )

    if not waitlist:
        return None

    next_passenger = waitlist[0]

    booking = Booking(
        ride_id=ride.id,
        passenger_id=next_passenger.passenger_id,
        status=BookingStatus.CONFIRMED,
    )

    decrease_available_seats(ride)

    try:

        db.add(booking)

        db.delete(next_passenger)

        db.commit()

        db.refresh(booking)

        create_notification(
            db=db,
            user_id=booking.passenger_id,
            title="Ride Available",
            message="You have been promoted from the waitlist.",
            notification_type=NotificationType.WAITLIST_PROMOTED,
        )

        create_audit_log(
            db=db,
            action="WAITLIST_PROMOTED",
            resource="Booking",
            user_id=booking.passenger_id,
            description=f"Passenger promoted to ride {ride.id}.",
        )

        recalculate_waitlist_positions(
            db=db,
            ride_id=ride.id,
        )

    except Exception:

        db.rollback()

        raise

    return booking


# ==========================================================
# Cancel Booking
# ==========================================================

def cancel_booking(
    db: Session,
    *,
    booking: Booking,
) -> Booking:
    """
    Cancel a booking and
    promote the next passenger
    if possible.
    """

    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled.",
        )

    ride = db.scalar(
        select(Ride).where(
            Ride.id == booking.ride_id
        )
    )

    if ride is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found.",
        )
    
    booking.status = BookingStatus.CANCELLED
    booking.cancelled_at = datetime.now(timezone.utc)  

    increase_available_seats(ride)

    try:

        db.commit()

        db.refresh(booking)

        create_notification(
            db=db,
            user_id=booking.passenger_id,
            title="Booking Cancelled",
            message="Your booking has been cancelled.",
            notification_type=NotificationType.RIDE_CANCELLED,
        )

        create_audit_log(
            db=db,
            action="BOOKING_CANCELLED",
            resource="Booking",
            user_id=booking.passenger_id,
            description=f"Booking #{booking.id} cancelled.",
        )

        if ride.available_seats > 0:

            promote_waitlist(
                db=db,
                ride=ride,
            )

    except Exception:

        db.rollback()

        raise

    return booking
    # ==========================================================
# Remove Passenger From Waitlist
# ==========================================================

def remove_from_waitlist(
    db: Session,
    *,
    ride_id: int,
    passenger_id: int,
) -> None:
    """
    Remove a passenger from a ride's waitlist.
    """

    stmt = select(Waitlist).where(
        Waitlist.ride_id == ride_id,
        Waitlist.passenger_id == passenger_id,
    )

    waitlist_entry = db.scalar(stmt)

    if waitlist_entry is None:
        return

    try:

        db.delete(waitlist_entry)

        db.commit()

        recalculate_waitlist_positions(
            db=db,
            ride_id=ride_id,
        )

    except Exception:

        db.rollback()

        raise


# ==========================================================
# Active Bookings
# ==========================================================

def get_active_bookings(
    db: Session,
    *,
    passenger_id: int,
) -> list[Booking]:
    """
    Return all active bookings
    for a passenger.
    """

    stmt = (
        select(Booking)
        .where(
            Booking.passenger_id == passenger_id,
            Booking.status == BookingStatus.CONFIRMED,
        )
        .order_by(
            Booking.created_at.desc()
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Booking Statistics
# ==========================================================

def get_booking_statistics(
    db: Session,
    *,
    passenger_id: int,
) -> dict[str, int]:
    """ 
    Return booking statistics
    for a passenger.
    """

    bookings = get_user_bookings(
        db,
        user_id=passenger_id,
    )

    confirmed = sum(
        1
        for booking in bookings
        if booking.status == BookingStatus.CONFIRMED
    )

    cancelled = sum(
        1
        for booking in bookings
        if booking.status == BookingStatus.CANCELLED
    )

    return {
        "total_bookings": len(bookings),
        "confirmed_bookings": confirmed,
        "cancelled_bookings": cancelled,
    }


# ==========================================================
# Ride Booking Count
# ==========================================================

def get_booking_count(
    db: Session,
    *,
    ride_id: int,
) -> int:
    """
    Return total confirmed bookings
    for a ride.
    """

    stmt = (
        select(func.count())
        .select_from(Booking)
        .where(
            Booking.ride_id == ride_id,
            Booking.status == BookingStatus.CONFIRMED,
        )
    )

    return db.scalar(stmt) or 0


# ==========================================================
# Passenger Waitlist Check
# ==========================================================

def is_passenger_in_waitlist(
    db: Session,
    *,
    ride_id: int,
    passenger_id: int,
) -> bool:
    """
    Check whether a passenger
    is already in the waitlist.
    """

    stmt = select(Waitlist).where(
        Waitlist.ride_id == ride_id,
        Waitlist.passenger_id == passenger_id,
    )

    return db.scalar(stmt) is not None


# ==========================================================
# Ride Full Check
# ==========================================================

def is_ride_full(
    ride: Ride,
) -> bool:
    """
    Returns True if the ride
    has no available seats.
    """

    return ride.available_seats <= 0


# ==========================================================
# Can Passenger Book Ride
# ==========================================================

def can_book_ride(
    db: Session,
    *,
    ride: Ride,
    passenger: User,
) -> bool:
    """
    Returns True if the passenger
    can book the ride.
    """

    check_driver_booking_own_ride(
        ride=ride,
        passenger=passenger,
    )

    check_duplicate_booking(
        db=db,
        ride_id=ride.id,
        passenger_id=passenger.id,
    )

    check_ride_availability(
        ride,
    )

    return True