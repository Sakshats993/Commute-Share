"""
==================================================
CommuteShare Database Base

Backend Internship Project
Bermer Software Private Limited

Imports all SQLAlchemy models so that
Alembic can discover them during
migration generation.

This file should only contain model imports
and the shared Base metadata.
==================================================
"""

from app.database.session import Base

# ==========================================================
# Import All Models
# ==========================================================

from app.models.audit_log import AuditLog
from app.models.booking import Booking
from app.models.notification import Notification
from app.models.rating import Rating
from app.models.ride import Ride
from app.models.sos_event import SOSEvent
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.waitlist import Waitlist

# ==========================================================
# Export
# ==========================================================

__all__ = [
    "Base",
    "User",
    "Vehicle",
    "Ride",
    "Booking",
    "Waitlist",
    "Rating",
    "Notification",
    "AuditLog",
    "SOSEvent",
]