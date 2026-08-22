from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.models.enums import RideStatus


class DriverInfo(BaseModel):
    id: int
    full_name: str
    email: str
    phone_number: Optional[str]
    profile_image: Optional[str]

    model_config = {
        "from_attributes": True,
    }


class VehicleInfo(BaseModel):
    id: int
    make: str
    model: str
    color: str
    registration_number: str
    seating_capacity: int

    model_config = {
        "from_attributes": True,
    }


class RideDetailsResponse(BaseModel):
    id: int

    pickup_location: str
    destination_location: str

    departure_time: datetime
    estimated_arrival_time: Optional[datetime]

    total_seats: int
    available_seats: int

    price_per_seat: Decimal

    notes: Optional[str]

    status: RideStatus

    driver: DriverInfo

    vehicle: VehicleInfo

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }