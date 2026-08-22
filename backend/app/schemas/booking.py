"""
==================================================
CommuteShare Booking Schemas

Backend Internship Project
Bermer Software Private Limited

Pydantic schemas related to bookings.

Includes:
- Booking Creation
- Booking Update
- Booking Response
==================================================
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import BookingStatus, RideStatus


# ======================================================
# Base Schema
# ======================================================

class BookingBase(BaseModel):
    """
    Common booking fields.
    """

    ride_id: int


# ======================================================
# Create Booking
# ======================================================

class BookingCreate(BookingBase):
    """
    Schema used when booking a ride.
    """

    pass


# ======================================================
# Update Booking
# ======================================================

class BookingUpdate(BaseModel):
    """
    Schema used to update a booking.
    """

    status: Optional[BookingStatus] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


# ======================================================
# Ride Summary
# ======================================================

class BookingRideSummary(BaseModel):
    id: int
    driver_id: int
    pickup_location: str
    destination_location: str
    departure_time: datetime
    status: RideStatus

    model_config = ConfigDict(
        from_attributes=True,
    )


# ======================================================
# Booking Response
# ======================================================

class BookingResponse(BookingBase):
    """
    Booking information returned by the API.
    """

    id: int
    
    passenger_id: int

    status: BookingStatus

    cancelled_at: Optional[datetime] = None

    created_at: datetime

    updated_at: datetime

    ride: BookingRideSummary

    model_config = ConfigDict(
        from_attributes=True,
    )