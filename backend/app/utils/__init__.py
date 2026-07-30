"""
==================================================
CommuteShare Utilities

Backend Internship Project
Bermer Software Private Limited

Provides reusable utility functions used
throughout the CommuteShare backend.

Utilities Included:
- Geolocation
- Logger
- Validators
==================================================
"""

from app.utils.geolocation import (
    format_distance,
    haversine_distance,
    is_within_radius,
)

from app.utils.logger import logger

from app.utils.validators import (
    validate_coordinates,
    validate_email,
    validate_password,
    validate_phone_number,
    validate_rating,
    validate_seat_count,
    validate_vehicle_number,
)

__all__ = [
    # Logger
    "logger",

    # Geolocation
    "haversine_distance",
    "is_within_radius",
    "format_distance",

    # Validators
    "validate_email",
    "validate_password",
    "validate_phone_number",
    "validate_vehicle_number",
    "validate_rating",
    "validate_seat_count",
    "validate_coordinates",
]