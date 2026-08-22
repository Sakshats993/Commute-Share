"""
==================================================
CommuteShare Ride Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- Create Ride
- View Rides
- Search Rides
- Update Ride
- Cancel Ride
==================================================
"""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.schemas.ride import RideSearchFilters

from app.core.deps import (
    get_current_active_user,
    get_db,
    require_driver,
)

from app.models.user import User

from app.schemas.ride import (
    RideCreate,
    RideResponse,
    RideUpdate,
)

from app.services.ride_service import (
    create_ride,
    delete_ride,
    get_available_rides,
    get_ride_by_id,
    search_rides,
    update_ride,
    end_ride,
    confirm_ride,
    start_ride,
)
from app.core.deps import require_passenger
from app.models.booking import Booking

from app.schemas.ride import QRVerificationRequest

from app.services.qr_service import (
    generate_boarding_qr,
    verify_boarding_qr,
)


router = APIRouter(
    prefix="/rides",
    tags=["Rides"],
)
# ==========================================================
# Create Ride
# ==========================================================

@router.post(
    "/",
    response_model=RideResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ride_route(
    ride_data: RideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    """
    Create a new ride.
    """

    return create_ride(
        db=db,
        driver=current_user,
        ride_data=ride_data,
    )
# ==========================================================
# Available Rides
# ==========================================================

@router.get(
    "/",
    response_model=list[RideResponse],
)
def get_rides(
    db: Session = Depends(get_db),
):
    """
    Return all available rides.
    """

    return get_available_rides(
        db=db,
    )
# ==========================================================
# Ride Details
# ==========================================================

@router.get(
    "/{ride_id}",
    response_model=RideResponse,
)
def get_ride(
    ride_id: int,
    db: Session = Depends(get_db),
):
    """
    Return ride details.
    """

    return get_ride_by_id(
        db=db,
        ride_id=ride_id,
    )
# ==========================================================
# Search Rides
# ==========================================================

@router.get(
    "/search/",
    response_model=list[RideResponse],
)
def search_available_rides(
    source: str = Query(...),
    destination: str = Query(...),
    db: Session = Depends(get_db),
):
    filters = RideSearchFilters(
        pickup_location=source,
        destination_location=destination,
    )

    return search_rides(
        db=db,
        filters=filters,
    )

# ==========================================================
# Generate Boarding QR
# ==========================================================
@router.post(
    "/{ride_id}/generate-qr",
)
def generate_qr(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    ride = get_ride_by_id(
         db=db,
        ride_id=ride_id,
    )

    if ride.driver_id != current_user.id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="You can only generate QR codes for your rides.",
        )

    token = generate_boarding_qr(
        ride=ride,
    )

    return {
        "qr_token": token,
    }

    # ==========================================================
    # Verify Boarding QR
    # ==========================================================

@router.post(
    "/verify-boarding",
    response_model=RideResponse,
)
def verify_qr(
    request: QRVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_passenger),
):
    return verify_boarding_qr(
            db=db,
            qr_token=request.qr_token,
            passenger_id=current_user.id,
        )
    # ==========================================================
# Update Ride
# ==========================================================

@router.put(
    "/{ride_id}",
    response_model=RideResponse,
)
def update_ride_route(
    ride_id: int,
    ride_data: RideUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    ride = get_ride_by_id(
        db=db,
        ride_id=ride_id,
    )

    if ride.driver_id != current_user.id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="You can only update your own rides.",
        )

    return update_ride(
        db=db,
        ride=ride,
        ride_data=ride_data,
    )

    # ==========================================================
    # Cancel Ride
    # ==========================================================
@router.delete(
    "/{ride_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ride_route(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    ride = get_ride_by_id(
            db=db,
            ride_id=ride_id,
    )

    if ride.driver_id != current_user.id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="You can only delete your own rides.",
        )

    delete_ride(
        db=db,
        ride=ride,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

# ==========================================================
# Start Ride
# ==========================================================

@router.patch(
    "/{ride_id}/start",
    response_model=RideResponse,
)
def start_ride_route(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    ride = get_ride_by_id(
        db=db,
        ride_id=ride_id,
    )

    return start_ride(
        db=db,
        ride=ride,
        driver=current_user,
    )


@router.patch(
    "/{ride_id}/end",
    response_model=RideResponse,
)
def end_ride_route(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    ride = get_ride_by_id(
        db=db,
        ride_id=ride_id,
    )

    return end_ride(
        db=db,
        ride=ride,
        driver=current_user,
    )

@router.patch(
    "/{ride_id}/confirm",
    response_model=RideResponse,
)
def confirm_ride_route(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_passenger),
):
    ride = get_ride_by_id(
        db=db,
        ride_id=ride_id,
    )

    return confirm_ride(
        db=db,
        ride=ride,
        passenger=current_user,
    )