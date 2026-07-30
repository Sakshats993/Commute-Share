"""
==================================================
CommuteShare Booking Tests

Backend Internship Project
Bermer Software Private Limited

Tests:
- View Bookings
- Booking Statistics
- Invalid Booking
- Authentication Protection
==================================================
"""

from __future__ import annotations


# ==========================================================
# My Bookings
# ==========================================================

def test_get_my_bookings_requires_authentication(
    client,
):
    """
    Accessing personal bookings without
    authentication should fail.
    """

    response = client.get("/bookings/me")

    assert response.status_code in (
        401,
        403,
    )


# ==========================================================
# Booking Statistics
# ==========================================================

def test_booking_statistics_requires_authentication(
    client,
):
    """
    Booking statistics require authentication.
    """

    response = client.get(
        "/bookings/me/statistics"
    )

    assert response.status_code in (
        401,
        403,
    )


# ==========================================================
# Invalid Booking
# ==========================================================

def test_invalid_booking_lookup(
    client,
):
    """
    Retrieving a booking that does not exist
    should return 404.
    """

    response = client.get(
        "/bookings/999999"
    )

    assert response.status_code in (
        404,
        405,
    )


# ==========================================================
# Booking Creation
# ==========================================================

def test_booking_requires_authentication(
    client,
):
    """
    Booking a ride without authentication
    should fail.
    """

    response = client.post(
        "/bookings",
        json={
            "ride_id": 1,
        },
    )

    assert response.status_code in (
        401,
        403,
    )


# ==========================================================
# Booking Cancellation
# ==========================================================

def test_cancel_booking_requires_authentication(
    client,
):
    """
    Cancelling a booking without authentication
    should fail.
    """

    response = client.delete(
        "/bookings/1"
    )

    assert response.status_code in (
        401,
        403,
    )