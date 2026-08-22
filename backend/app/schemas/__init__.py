"""
==================================================
CommuteShare Schemas Package

Backend Internship Project
Bermer Software Private Limited

Exports all Pydantic schemas used throughout
the CommuteShare backend.
==================================================
"""

# Authentication
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    Token,
    TokenPayload,
)

# User
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPublic,
    UserResponse,
)

# Vehicle
from app.schemas.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
)

# Ride
from app.schemas.ride import (
    RideCreate,
    RideUpdate,
    RideResponse,
    RideSearchFilters,
    QRVerificationRequest,
)

# Booking
from app.schemas.booking import (
    BookingBase,
    BookingCreate,
    BookingUpdate,
    BookingResponse,
)

# Miscellaneous
from app.schemas.misc import (
    RatingCreate,
    RatingResponse,
    NotificationResponse,
    WaitlistResponse,
    SOSCreate,
    SOSResponse,
    AdminDashboardResponse,
    MessageResponse,
)

__all__ = [
    # Authentication
    "LoginRequest",
    "LoginResponse",
    "Token",
    "TokenPayload",

    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UserResponse",

    # Vehicle
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",

    # Ride
    # Ride
    "RideCreate",
    "RideUpdate",
    "RideResponse",
    "RideSearchFilters",
    "QRVerificationRequest",

    # Booking
    "BookingBase",
    "BookingCreate",
    "BookingUpdate",
    "BookingResponse",

    # Miscellaneous
    "RatingCreate",
    "RatingResponse",
    "NotificationResponse",
    "WaitlistResponse",
    "SOSCreate",
    "SOSResponse",
    "AdminDashboardResponse",
    "MessageResponse",
]