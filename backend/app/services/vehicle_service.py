"""
==================================================
CommuteShare Vehicle Service

Backend Internship Project
Bermer Software Private Limited

Handles:
- Vehicle Registration
- Vehicle Retrieval
- Vehicle Updates
- Vehicle Deletion
==================================================
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.models.user import User

from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
)


# ==========================================================
# Get Vehicle By ID
# ==========================================================

def get_vehicle_by_id(
    db: Session,
    *,
    vehicle_id: int,
) -> Vehicle:
    """
    Return a vehicle by ID.
    """

    stmt = select(Vehicle).where(
        Vehicle.id == vehicle_id
    )

    vehicle = db.scalar(stmt)

    if vehicle is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )

    return vehicle


# ==========================================================
# Get User Vehicles
# ==========================================================

def get_user_vehicles(
    db: Session,
    *,
    owner_id: int,
) -> list[Vehicle]:
    """
    Return all vehicles owned by a user.
    """

    stmt = (
        select(Vehicle)
        .where(
            Vehicle.owner_id == owner_id
        )
        .order_by(
            Vehicle.created_at.desc()
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Create Vehicle
# ==========================================================

def create_vehicle(
    db: Session,
    *,
    owner: User,
    vehicle_data: VehicleCreate,
) -> Vehicle:
    """
    Register a new vehicle.
    """

    vehicle = Vehicle(
        owner_id=owner.id,
        **vehicle_data.model_dump(),
    )

    try:

        db.add(vehicle)

        db.commit()

        db.refresh(vehicle)

    except Exception:

        db.rollback()

        raise

    return vehicle


# ==========================================================
# Update Vehicle
# ==========================================================

def update_vehicle(
    db: Session,
    *,
    vehicle_id: int,
    owner: User,
    vehicle_data: VehicleUpdate,
) -> Vehicle:
    """
    Update an existing vehicle.
    """

    vehicle = get_vehicle_by_id(
        db=db,
        vehicle_id=vehicle_id,
    )

    if vehicle.owner_id != owner.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this vehicle.",
        )

    update_data = vehicle_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():

        setattr(
            vehicle,
            field,
            value,
        )

    try:

        db.commit()

        db.refresh(vehicle)

    except Exception:

        db.rollback()

        raise

    return vehicle


# ==========================================================
# Delete Vehicle
# ==========================================================

def delete_vehicle(
    db: Session,
    *,
    vehicle_id: int,
    owner: User,
) -> None:
    """
    Delete a vehicle.
    """

    vehicle = get_vehicle_by_id(
        db=db,
        vehicle_id=vehicle_id,
    )

    if vehicle.owner_id != owner.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this vehicle.",
        )

    try:

        vehicle.is_active = False
        db.commit()

    except Exception:

        db.rollback()

        raise