"""
==================================================
CommuteShare Ride Schemas

Backend Internship Project
Bermer Software Private Limited

Pydantic schemas related to rides.

Includes:
- Ride Creation
- Ride Update
- Ride Response
- Ride Search Filters
==================================================
"""

from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import RideStatus

# ======================================================
# Driver Summary
# ======================================================

class DriverSummary(BaseModel):
    """
    Driver information returned with a ride.
    """

    id: int

    full_name: str

    average_rating: float

    review_count: int

    completed_rides: int

    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

# ======================================================
# Vehicle Summary
# ======================================================

class VehicleSummary(BaseModel):
    """
    Vehicle information returned with a ride.
    """

    id: int
    make: str
    model: str
    color: str
    registration_number: str
    seating_capacity: int

    model_config = ConfigDict(
        from_attributes=True,
    )

# ======================================================
# Create Ride
# ======================================================

class RideCreate(BaseModel):
    vehicle_make: str = Field(..., min_length=1, max_length=50)
    vehicle_model: str = Field(..., min_length=1, max_length=50)
    vehicle_color: str = Field(..., min_length=1, max_length=30)
    registration_number: str = Field(..., min_length=1, max_length=20)
    vehicle_seating_capacity: int = Field(..., ge=2, le=100)

    pickup_location: str = Field(..., min_length=1, max_length=255)
    pickup_latitude: float = Field(..., ge=-90, le=90, allow_inf_nan=False)
    pickup_longitude: float = Field(..., ge=-180, le=180, allow_inf_nan=False)

    destination_location: str = Field(..., min_length=1, max_length=255)
    destination_latitude: float = Field(..., ge=-90, le=90, allow_inf_nan=False)
    destination_longitude: float = Field(..., ge=-180, le=180, allow_inf_nan=False)

    departure_time: datetime
    estimated_arrival_time: Optional[datetime] = None

    total_seats: int = Field(..., ge=1, le=99)
    price_per_seat: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    notes: Optional[str] = Field(default=None, max_length=2000)


# ======================================================
# ======================================================
# Update Ride
# ======================================================

class RideUpdate(BaseModel):
    """
    Schema used to update ride details.
    """

    pickup_location: Optional[str] = Field(default=None, min_length=1, max_length=255)
    pickup_latitude: Optional[float] = Field(default=None, ge=-90, le=90, allow_inf_nan=False)
    pickup_longitude: Optional[float] = Field(default=None, ge=-180, le=180, allow_inf_nan=False)

    destination_location: Optional[str] = Field(default=None, min_length=1, max_length=255)
    destination_latitude: Optional[float] = Field(default=None, ge=-90, le=90, allow_inf_nan=False)
    destination_longitude: Optional[float] = Field(default=None, ge=-180, le=180, allow_inf_nan=False)

    departure_time: Optional[datetime] = None
    estimated_arrival_time: Optional[datetime] = None

    total_seats: Optional[int] = Field(default=None, ge=1, le=99)
    price_per_seat: Optional[Decimal] = Field(default=None, ge=0, max_digits=10, decimal_places=2)

    notes: Optional[str] = Field(default=None, max_length=2000)

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )
# ======================================================
# Ride Response
# ======================================================
class RideResponse(BaseModel):
    id: int
    driver_id: int

    driver: DriverSummary
    vehicle: VehicleSummary

    pickup_location: str
    pickup_latitude: float
    pickup_longitude: float

    destination_location: str
    destination_latitude: float
    destination_longitude: float

    departure_time: datetime
    estimated_arrival_time: Optional[datetime]

    total_seats: int
    available_seats: int
    price_per_seat: Decimal
    notes: Optional[str]

    status: RideStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

# ======================================================
# Ride Search Filters
# ======================================================

class RideSearchFilters(BaseModel):
    """
    Filters used when searching for rides.
    """

    pickup_location: Optional[str] = None

    destination_location: Optional[str] = None

    departure_date: Optional[datetime] = None

    minimum_available_seats: Optional[int] = Field(
        default=None,
        ge=1,
    )

    maximum_price: Optional[Decimal] = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    sort_by: Literal["departure_time", "price"] = "departure_time"
# ======================================================
# QR Boarding
# ======================================================

class QRVerificationRequest(BaseModel):
    """
    Passenger QR verification request.
    """

    qr_token: str
