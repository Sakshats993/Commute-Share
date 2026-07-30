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

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.enums import RideStatus
from app.models.ride import Ride
from app.models.user import User
from app.models.vehicle import Vehicle

from app.schemas.ride import (
    RideCreate,
    RideSearchFilters,
    RideUpdate,
)

from app.services.audit_service import create_audit_log


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

    stmt = select(Ride).where(Ride.id == ride_id)

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
            Vehicle.id == ride_data.vehicle_id,
            Vehicle.owner_id == driver.id,
            Vehicle.is_active.is_(True),
        )
    )

    if vehicle is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )

    ride = Ride(
        driver_id=driver.id,
        vehicle_id=ride_data.vehicle_id,

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

    for field, value in update_data.items():

        setattr(
            ride,
            field,
            value,
        )

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

    stmt = select(Ride)

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