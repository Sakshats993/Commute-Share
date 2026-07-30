"""
==================================================
CommuteShare Matching Service

Backend Internship Project
Bermer Software Private Limited

Handles ride matching functionality.

Features:
- Nearby Ride Search
- Distance Calculation
- Ride Filtering
- Ride Sorting
==================================================
"""

from __future__ import annotations

from math import atan2, cos, radians, sin, sqrt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import RideStatus
from app.models.ride import Ride


# ======================================================
# Haversine Distance
# ======================================================

def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate distance (km) between two coordinates.
    """

    earth_radius = 6371

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(d_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a),
    )

    return earth_radius * c


# ======================================================
# Nearby Ride Search
# ======================================================

def find_nearby_rides(
    db: Session,
    *,
    latitude: float,
    longitude: float,
    radius_km: float = 5.0,
) -> list[Ride]:
    """
    Find rides within a given radius.
    """

    stmt = select(Ride).where(
        Ride.status == RideStatus.SCHEDULED,
        Ride.available_seats > 0,
    )

    rides = list(db.scalars(stmt).all())

    nearby = []

    for ride in rides:

        distance = calculate_distance(
            latitude,
            longitude,
            ride.pickup_latitude,
            ride.pickup_longitude,
        )

        if distance <= radius_km:

            setattr(
                ride,
                "distance",
                round(distance, 2),
            )

            nearby.append(ride)

    nearby.sort(
        key=lambda ride: ride.distance,
    )

    return nearby


# ======================================================
# Filter Available Rides
# ======================================================

def filter_available_rides(
    rides: list[Ride],
) -> list[Ride]:
    """
    Return only rides with available seats.
    """

    return [
        ride
        for ride in rides
        if (
            ride.available_seats > 0
            and ride.status == RideStatus.SCHEDULED
        )
    ]


# ======================================================
# Sort By Distance
# ======================================================

def sort_by_distance(
    rides: list[Ride],
) -> list[Ride]:
    """
    Sort rides by nearest pickup.
    """

    return sorted(
        rides,
        key=lambda ride: getattr(
            ride,
            "distance",
            float("inf"),
        ),
    )


# ======================================================
# Sort By Departure Time
# ======================================================

def sort_by_departure(
    rides: list[Ride],
) -> list[Ride]:
    """
    Sort rides by departure time.
    """

    return sorted(
        rides,
        key=lambda ride: ride.departure_time,
    )