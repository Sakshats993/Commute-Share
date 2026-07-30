"""
==================================================
CommuteShare Enumerations

Backend Internship Project
Bermer Software Private Limited

Centralized enumerations used throughout the
database models.
==================================================
"""

from enum import Enum


class UserRole(str, Enum):
    """
    Roles available within the application.
    """

    ADMIN = "admin"
    DRIVER = "driver"
    PASSENGER = "passenger"


class RideStatus(str, Enum):
    """
    Current state of a ride.
    """

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BookingStatus(str, Enum):
    """
    Current state of a booking.
    """

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"


class NotificationType(str, Enum):
    """
    Notification categories.
    """

    RIDE_BOOKED = "ride_booked"
    BOOKING_CONFIRMED = "booking_confirmed"
    WAITLIST_PROMOTED = "waitlist_promoted"
    RIDE_CANCELLED = "ride_cancelled"
    RATING_RECEIVED = "rating_received"
    SOS_TRIGGERED = "sos_triggered"

class SOSStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"