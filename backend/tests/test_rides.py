"""
==================================================
CommuteShare Ride Tests

Backend Internship Project
Bermer Software Private Limited

Tests:
- Get Available Rides
- Get Ride By ID
- Search Rides
- Unauthorized Ride Creation
==================================================
"""

from __future__ import annotations


# ==========================================================
# Get Available Rides
# ==========================================================

def test_get_available_rides(client):
    """
    Verify available rides endpoint.
    """

    response = client.get("/rides")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


# ==========================================================
# Search Rides
# ==========================================================

def test_search_rides(client):
    """
    Search rides.
    """

    response = client.get(
        "/rides/search",
        params={
            "source": "Udupi",
            "destination": "Manipal",
        },
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


# ==========================================================
# Invalid Ride
# ==========================================================

def test_get_invalid_ride(client):
    """
    Request a ride that does not exist.
    """

    response = client.get(
        "/rides/999999"
    )

    assert response.status_code == 404


# ==========================================================
# Unauthorized Ride Creation
# ==========================================================

def test_create_ride_requires_authentication(
    client,
):
    """
    Creating a ride without authentication
    should fail.
    """

    response = client.post(
        "/rides",
        json={
            "source": "Udupi",
            "destination": "Mangalore",
            "departure_time": "2026-08-01T09:00:00",
            "available_seats": 3,
            "price": 250,
            "vehicle_id": 1,
        },
    )

    assert response.status_code in (
        401,
        403,
    )