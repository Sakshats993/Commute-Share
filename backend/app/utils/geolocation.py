"""
==================================================
CommuteShare Geolocation Utilities

Backend Internship Project
Bermer Software Private Limited

Provides reusable geolocation utilities.

Features:
- Haversine Distance
- Coordinate Validation
- Radius Checks
==================================================
"""

from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0


# ==========================================================
# Degrees to Radians
# ==========================================================

def _to_radians(degrees: float) -> float:
    """
    Convert degrees to radians.
    """

    return math.radians(degrees)


# ==========================================================
# Haversine Distance
# ==========================================================

def haversine_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> float:
    """
    Calculate the great-circle distance
    between two coordinates.

    Returns:
        Distance in kilometers.
    """

    lat1 = _to_radians(latitude1)
    lon1 = _to_radians(longitude1)

    lat2 = _to_radians(latitude2)
    lon2 = _to_radians(longitude2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return EARTH_RADIUS_KM * c


# ==========================================================
# Radius Check
# ==========================================================

def is_within_radius(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
    radius_km: float,
) -> bool:
    """
    Check whether two coordinates are
    within a specified radius.
    """

    return (
        haversine_distance(
            latitude1,
            longitude1,
            latitude2,
            longitude2,
        )
        <= radius_km
    )


# ==========================================================
# Distance Formatter
# ==========================================================

def format_distance(
    distance_km: float,
) -> str:
    """
    Format a distance for display.
    """

    if distance_km < 1:

        return f"{distance_km * 1000:.0f} m"

    return f"{distance_km:.2f} km"


# ==========================================================
# Export
# ==========================================================

__all__ = [
    "haversine_distance",
    "is_within_radius",
    "format_distance",
]