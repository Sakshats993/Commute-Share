"""
==================================================
CommuteShare Vehicle Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- Register Vehicle
- View Vehicles
- Update Vehicle
- Delete Vehicle
==================================================
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_active_user,
    get_db,
    require_driver,
)

from app.models.user import User

from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
)

from app.services.vehicle_service import (
    create_vehicle,
    delete_vehicle,
    get_user_vehicles,
    get_vehicle_by_id,
    update_vehicle,
)

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)
# ==========================================================
# Register Vehicle
# ==========================================================

@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    """
    Register a new vehicle.
    """

    return create_vehicle(
        db=db,
        owner=current_user,
        vehicle_data=vehicle_data,
    )
# ==========================================================
# Get My Vehicles
# ==========================================================

@router.get(
    "/",
    response_model=list[VehicleResponse],
)
def get_my_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return all vehicles owned by the current user.
    """

    return get_user_vehicles(
        db=db,
        owner_id=current_user.id,
    )
# ==========================================================
# Get Vehicle
# ==========================================================

@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a vehicle by ID.
    """

    return get_vehicle_by_id(
        db=db,
        vehicle_id=vehicle_id,
    )
# ==========================================================
# Update Vehicle
# ==========================================================

@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle_route(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    """
    Update vehicle details.
    """

    return update_vehicle(
        db=db,
        vehicle_id=vehicle_id,
        owner=current_user,
        vehicle_data=vehicle_data,
    )
# ==========================================================
# Delete Vehicle
# ==========================================================

@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vehicle_route(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    """
    Delete a vehicle.
    """

    delete_vehicle(
        db=db,
        vehicle_id=vehicle_id,
        owner=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )