"""
==================================================
CommuteShare Miscellaneous Schemas

Backend Internship Project
Bermer Software Private Limited

Contains schemas for:

- Ratings
- Notifications
- Waitlist
- SOS Events
- Admin Dashboard
==================================================
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import NotificationType, SOSStatus


# ======================================================
# Rating Schemas
# ======================================================
class RatingCreate(BaseModel):
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(
        None,
        max_length=500,
    )


# ======================================================
# Rating Update
# ======================================================


class RatingUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review: Optional[str] = Field(None, max_length=500)


class RatingResponse(BaseModel):
    id: int
    ride_id: int
    reviewer_id: int
    reviewer_name: str
    reviewer_role: str
    reviewee_id: int
    rating: int
    review: Optional[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class RatingCandidateResponse(BaseModel):
    booking_id: int
    ride_id: int

    reviewee_id: int
    reviewee_name: str
    reviewee_role: str

    pickup_location: str
    destination_location: str
    departure_time: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

# ======================================================
# Notification Schemas
# ======================================================

class NotificationResponse(BaseModel):
    """
    Notification returned by the API.
    """

    id: int

    title: str

    message: str

    type: NotificationType

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ======================================================
# Waitlist Schemas
# ======================================================

class WaitlistResponse(BaseModel):
    """
    Waitlist information.
    """

    id: int

    ride_id: int

    passenger_id: int

    queue_position: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ======================================================
# SOS Schemas
# ======================================================
class SOSCreate(BaseModel):
    """
    Create an SOS event.

    The user only needs to trigger the SOS.
    Ride context and emergency details can be
    determined by the backend.
    """

    ride_id: Optional[int] = None

    emergency_type: str = Field(
        default="Emergency",
        max_length=100,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
    )

# ======================================================
# SOS Response
# ======================================================

class SOSResponse(BaseModel):
    """
    SOS event returned by the API.
    """

    id: int

    user_id: int

    ride_id: Optional[int] = None

    emergency_type: str

    description: Optional[str] = None

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    status: SOSStatus

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

# ======================================================
# Admin Dashboard
# ======================================================

class AdminDashboardResponse(BaseModel):
    """
    Summary statistics shown on the admin dashboard.
    """

    total_users: int

    total_drivers: int

    total_passengers: int

    total_rides: int

    total_bookings: int

    active_rides: int

    active_sos_events: int

    pending_waitlist_entries: int

# ======================================================
# Generic Message Response
# ======================================================

class MessageResponse(BaseModel):
    """
    Generic success or informational message.
    """

    message: str