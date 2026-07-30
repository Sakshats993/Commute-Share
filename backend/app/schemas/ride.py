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
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import RideStatus


# ======================================================
# Base Schema
# ======================================================

class RideBase(BaseModel):
    """
    Common ride fields.
    """

    vehicle_id: int

    pickup_location: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    pickup_latitude: float = Field(
        ...,
        ge=-90,
        le=90,
    )

    pickup_longitude: float = Field(
        ...,
        ge=-180,
        le=180,
    )

    destination_location: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    destination_latitude: float = Field(
        ...,
        ge=-90,
        le=90,
    )

    destination_longitude: float = Field(
        ...,
        ge=-180,
        le=180,
    )

    departure_time: datetime

    estimated_arrival_time: Optional[datetime] = None

    total_seats: int = Field(
        ...,
        ge=1,
        le=10,
    )

    price_per_seat: Decimal = Field(
        ...,
        ge=0,
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# ======================================================
# Create Ride
# ======================================================

class RideCreate(RideBase):
    """
    Schema used when creating a ride.
    """

    pass


# ======================================================
# Update Ride
# ======================================================

class RideUpdate(BaseModel):
    """
    Schema used to update ride details.
    """

    vehicle_id: Optional[int] = None

    pickup_location: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    pickup_latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
    )

    pickup_longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
    )

    destination_location: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    destination_latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
    )

    destination_longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
    )

    departure_time: Optional[datetime] = None

    estimated_arrival_time: Optional[datetime] = None

    total_seats: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
    )

    price_per_seat: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    status: Optional[RideStatus] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


# ======================================================
# Ride Response
# ======================================================

class RideResponse(RideBase):
    """
    Ride information returned by the API.
    """

    id: int

    driver_id: int

    available_seats: int

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
    )