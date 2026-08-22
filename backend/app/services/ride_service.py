"""
==================================================
CommuteShare Ride Service

Backend Internship Project
Bermer Software Private Limited

Handles:

- Create Ride
- Update Ride
- Delete Ride
- Get Ride
- List Rides
- Search Rides
==================================================
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from fastapi import HTTPException, status

from app.models.enums import (
    RideStatus,
    BookingStatus,
)
from app.models.ride import Ride
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.enums import PaymentStatus

from app.schemas.ride import (
    RideCreate,
    RideSearchFilters,
    RideUpdate,
)

from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification
from app.models.enums import NotificationType
from app.models.booking import Booking
from app.models.enums import BookingStatus
from app.models.notification import Notification


# ======================================================
# Get Ride By ID
# ======================================================

def get_ride_by_id(
    db: Session,
    ride_id: int,
) -> Ride:
    """
    Return a ride by its ID.
    """

    stmt = (
    select(Ride)
    .options(
        selectinload(Ride.driver),
        selectinload(Ride.vehicle),
    )
    .where(Ride.id == ride_id)
)

    ride = db.scalar(stmt)

    if ride is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found.",
        )

    return ride


# ======================================================
# Create Ride
# ======================================================

def create_ride(
    db: Session,
    *,
    driver: User,
    ride_data: RideCreate,
) -> Ride:
    """
    Create a new ride.
    """
    vehicle = db.scalar(
        select(Vehicle).where(
            Vehicle.owner_id == driver.id,
            Vehicle.registration_number == ride_data.registration_number,
        )
    )

    if vehicle:
        vehicle.is_active = True
    else:
        vehicle = Vehicle(...)
        db.add(vehicle)
        db.flush()
    

    print("Vehicle found:", vehicle)
    print("Driver ID:", driver.id)
    print("Registration:", ride_data.registration_number)

    if vehicle is None:

        vehicle = Vehicle(
            owner_id=driver.id,
            make=ride_data.vehicle_make,
            model=ride_data.vehicle_model,
            color=ride_data.vehicle_color,
            registration_number=ride_data.registration_number,
            seating_capacity=ride_data.vehicle_seating_capacity,
            is_active=True,
        )

        db.add(vehicle)

        # Generate vehicle.id without committing
        db.flush()

    ride = Ride(
        driver_id=driver.id,
        vehicle_id=vehicle.id,

        pickup_location=ride_data.pickup_location,
        pickup_latitude=ride_data.pickup_latitude,
        pickup_longitude=ride_data.pickup_longitude,

        destination_location=ride_data.destination_location,
        destination_latitude=ride_data.destination_latitude,
        destination_longitude=ride_data.destination_longitude,

        departure_time=ride_data.departure_time,
        estimated_arrival_time=ride_data.estimated_arrival_time,

        total_seats=ride_data.total_seats,
        available_seats=ride_data.total_seats,

        price_per_seat=ride_data.price_per_seat,

        notes=ride_data.notes,

        status=RideStatus.SCHEDULED,
    )

    try:

        db.add(ride)

        db.commit()

        db.refresh(ride)

        create_audit_log(
            db=db,
            action="CREATE",
            resource="Ride",
            user_id=driver.id,
            description=f"Ride {ride.id} created.",
        )

    except Exception:

        db.rollback()

        raise

    return ride


# ======================================================
# Update Ride
# ======================================================
# ======================================================
# Update Ride
# ======================================================

def update_ride(
    db: Session,
    *,
    ride: Ride,
    ride_data: RideUpdate,
) -> Ride:
    """
    Update an existing ride.
    """

    update_data = ride_data.model_dump(
        exclude_unset=True
    )

    # Remember previous status
    previous_status = ride.status

    for field, value in update_data.items():

        setattr(
            ride,
            field,
            value,
        )

    # Ride completed for the first time
    if (
        previous_status != RideStatus.COMPLETED
        and ride.status == RideStatus.COMPLETED
    ):
        ride.driver.completed_rides += 1

    try:

        db.commit()

        db.refresh(ride)

    except Exception:

        db.rollback()

        raise

    return ride


# ======================================================
# Delete Ride
# ======================================================

def delete_ride(
    db: Session,
    *,
    ride: Ride,
) -> None:
    """
    Delete a ride.
    """

    try:

        db.delete(ride)

        db.commit()

    except Exception:

        db.rollback()

        raise


# ======================================================
# List All Scheduled Rides
# ======================================================

def get_available_rides(
    db: Session,
) -> list[Ride]:
    """
    Return all scheduled rides.
    """

    stmt = (
    select(Ride)
    .options(
        selectinload(Ride.driver),
        selectinload(Ride.vehicle),
    )
    .where(
        Ride.status == RideStatus.SCHEDULED
    )
    .order_by(
        Ride.departure_time
    )
)

    return list(
        db.scalars(stmt).all()
    )


# ======================================================
# Search Rides
# ======================================================

def search_rides(
    db: Session,
    filters: RideSearchFilters,
) -> list[Ride]:
    """
    Search rides using filters.
    """

    stmt = (
    select(Ride)
    .options(
        selectinload(Ride.driver),
        selectinload(Ride.vehicle),
    )
)

    if filters.pickup_location:

        stmt = stmt.where(
            Ride.pickup_location.ilike(
                f"%{filters.pickup_location}%"
            )
        )

    if filters.destination_location:

        stmt = stmt.where(
            Ride.destination_location.ilike(
                f"%{filters.destination_location}%"
            )
        )

    if filters.departure_date:

        stmt = stmt.where(
            Ride.departure_time >=
            filters.departure_date
        )

    if filters.maximum_price:

        stmt = stmt.where(
            Ride.price_per_seat <=
            filters.maximum_price
        )

    if filters.minimum_available_seats:

        stmt = stmt.where(
            Ride.available_seats >=
            filters.minimum_available_seats
        )

    stmt = stmt.where(
        Ride.status == RideStatus.SCHEDULED
    )

    stmt = stmt.order_by(
        Ride.departure_time
    )

    return list(
        db.scalars(stmt).all()
    )

# ======================================================
# Driver Starts Ride
# ======================================================

def start_ride(
    db: Session,
    *,
    ride: Ride,
    driver: User,
) -> Ride:
    """
    Driver starts the ride.
    """

    if ride.driver_id != driver.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only start your own rides.",
        )

    if ride.status != RideStatus.SCHEDULED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride cannot be started in its current state.",
        )

    confirmed_bookings = db.scalars(
        select(Booking).where(
            Booking.ride_id == ride.id,
            Booking.status == BookingStatus.CONFIRMED,
        )
    ).all()

    if not confirmed_bookings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one passenger must be confirmed before starting the ride.",
        )

    ride.status = RideStatus.IN_PROGRESS

    try:
        db.commit()
        db.refresh(ride)

        return ride

    except Exception:
        db.rollback()
        raise
# ======================================================
# Driver Ends Ride
# ======================================================
def end_ride(
    db: Session,
    *,
    ride: Ride,
    driver: User,
) -> Ride:
    """
    Driver marks the ride as finished.
    """

    if ride.driver_id != driver.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only end your own rides.",
        )

    if ride.status != RideStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride is not in progress.",
        )

    ride.driver_completed_at = datetime.now(
        timezone.utc
    )

    ride.status = (
        RideStatus.AWAITING_PASSENGER_CONFIRMATION
    )

    try:
        db.commit()
        db.refresh(ride)

        return ride

    except Exception as e:
        print("END RIDE ERROR:", repr(e))
        db.rollback()
        raise

# ======================================================
# Passenger Confirms Ride
# ======================================================
def confirm_ride(
    db: Session,
    *,
    ride: Ride,
    passenger: User,
) -> Ride:
    """
    Passenger confirms that the ride has ended.
    """

    booking = db.scalar(
        select(Booking).where(
            Booking.ride_id == ride.id,
            Booking.passenger_id == passenger.id,
            Booking.status == BookingStatus.CONFIRMED,
        )
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not booked for this ride.",
        )

    if (
        ride.status
        != RideStatus.AWAITING_PASSENGER_CONFIRMATION
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride is not awaiting confirmation.",
        )

    booking.has_confirmed_dropoff = True

    ride.passenger_completed_at = datetime.now(
        timezone.utc,
    )

    ride.completed_at = datetime.now(
        timezone.utc,
    )

    ride.status = RideStatus.COMPLETED

    ride.driver.completed_rides += 1

    existing_payment = db.scalar(
        select(Payment).where(
            Payment.booking_id == booking.id
        )
    )

    if existing_payment is None:
        payment = Payment(
            ride_id=ride.id,
            booking_id=booking.id,
            amount=ride.price_per_seat,
            status=PaymentStatus.UNPAID,
        )

        db.add(payment)

    db.commit()

    db.refresh(ride)

    return ride