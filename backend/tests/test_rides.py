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

from datetime import datetime, timedelta, timezone

from app.core.security import create_access_token
from app.models.enums import UserRole
from app.models.user import User


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


def test_create_ride_with_new_vehicle_succeeds(client, db):
    driver = User(
        full_name="Driver One",
        email="driver-one@example.com",
        password_hash="test-hash",
        role=UserRole.DRIVER,
    )
    db.add(driver)
    db.commit()
    token = create_access_token(driver.email)
    payload = {
        "vehicle_make": "Test Motors",
        "vehicle_model": "City",
        "vehicle_color": "Blue",
        "registration_number": "TEST-1001",
        "vehicle_seating_capacity": 5,
        "pickup_location": "Udupi",
        "pickup_latitude": 13.3409,
        "pickup_longitude": 74.7421,
        "destination_location": "Manipal",
        "destination_latitude": 13.35,
        "destination_longitude": 74.79,
        "departure_time": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        "total_seats": 4,
        "price_per_seat": "125.50",
    }

    response = client.post(
        "/rides",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["total_seats"] == 4
    assert data["available_seats"] == 4
    assert data["vehicle"]["seating_capacity"] == 5
    assert data["price_per_seat"] == "125.50"
    assert "email" not in data["driver"]


def test_create_ride_rejects_seats_above_vehicle_capacity(client, db):
    driver = User(
        full_name="Driver Two",
        email="driver-two@example.com",
        password_hash="test-hash",
        role=UserRole.DRIVER,
    )
    db.add(driver)
    db.commit()
    token = create_access_token(driver.email)
    payload = {
        "vehicle_make": "Test Motors",
        "vehicle_model": "City",
        "vehicle_color": "Blue",
        "registration_number": "TEST-1002",
        "vehicle_seating_capacity": 5,
        "pickup_location": "Udupi",
        "pickup_latitude": 13.3409,
        "pickup_longitude": 74.7421,
        "destination_location": "Manipal",
        "destination_latitude": 13.35,
        "destination_longitude": 74.79,
        "departure_time": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        "total_seats": 5,
        "price_per_seat": "125.50",
    }

    response = client.post(
        "/rides",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
    assert "vehicle capacity" in response.json()["detail"]


def test_update_ride_accepts_only_editable_fields(client, db):
    driver = User(
        full_name="Driver Edit",
        email="driver-edit@example.com",
        password_hash="test-hash",
        role=UserRole.DRIVER,
    )
    db.add(driver)
    db.commit()
    token = create_access_token(driver.email)
    headers = {"Authorization": f"Bearer {token}"}
    create_payload = {
        "vehicle_make": "Test Motors", "vehicle_model": "City", "vehicle_color": "Blue",
        "registration_number": "TEST-EDIT", "vehicle_seating_capacity": 5,
        "pickup_location": "Udupi", "pickup_latitude": 13.34, "pickup_longitude": 74.74,
        "destination_location": "Manipal", "destination_latitude": 13.35,
        "destination_longitude": 74.79,
        "departure_time": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        "total_seats": 4, "price_per_seat": "125.50",
    }
    created = client.post("/rides/", json=create_payload, headers=headers)
    assert created.status_code == 201, created.text

    updated = client.put(
        f"/rides/{created.json()['id']}",
        json={"pickup_location": "Updated Udupi", "price_per_seat": "130.00"},
        headers=headers,
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["pickup_location"] == "Updated Udupi"
    assert updated.json()["price_per_seat"] == "130.00"

    forbidden_status_change = client.put(
        f"/rides/{created.json()['id']}",
        json={"status": "completed"},
        headers=headers,
    )
    assert forbidden_status_change.status_code == 422


def test_driver_to_passenger_booking_and_cancellation_workflow(client):
    driver_signup = client.post("/auth/register", json={
        "full_name": "Workflow Driver", "email": "workflow-driver@example.com",
        "password": "Password123", "phone_number": "9876501234", "role": "driver",
    })
    assert driver_signup.status_code == 201, driver_signup.text
    driver_login = client.post("/auth/login", data={
        "username": "workflow-driver@example.com", "password": "Password123",
    })
    assert driver_login.status_code == 200, driver_login.text
    driver_headers = {"Authorization": f"Bearer {driver_login.json()['access_token']}"}
    ride_response = client.post("/rides/", headers=driver_headers, json={
        "vehicle_make": "Test Motors", "vehicle_model": "City", "vehicle_color": "Blue",
        "registration_number": "TEST-FLOW", "vehicle_seating_capacity": 5,
        "pickup_location": "Udupi", "pickup_latitude": 13.34, "pickup_longitude": 74.74,
        "destination_location": "Manipal", "destination_latitude": 13.35,
        "destination_longitude": 74.79,
        "departure_time": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        "total_seats": 1, "price_per_seat": "125.50",
    })
    assert ride_response.status_code == 201, ride_response.text
    ride_id = ride_response.json()["id"]

    passenger_signup = client.post("/auth/register", json={
        "full_name": "Workflow Passenger", "email": "workflow-passenger@example.com",
        "password": "Password123", "phone_number": "9876501235", "role": "passenger",
    })
    assert passenger_signup.status_code == 201, passenger_signup.text
    passenger_login = client.post("/auth/login", data={
        "username": "workflow-passenger@example.com", "password": "Password123",
    })
    assert passenger_login.status_code == 200, passenger_login.text
    passenger_headers = {"Authorization": f"Bearer {passenger_login.json()['access_token']}"}

    booking = client.post("/bookings/", headers=passenger_headers, json={"ride_id": ride_id})
    assert booking.status_code == 201, booking.text
    assert booking.json()["ride"]["id"] == ride_id
    assert len(client.get("/bookings/me", headers=passenger_headers).json()) == 1
    cancelled = client.delete(f"/bookings/{booking.json()['id']}", headers=passenger_headers)
    assert cancelled.status_code == 204
    passenger_bookings = client.get("/bookings/me", headers=passenger_headers).json()
    assert len(passenger_bookings) == 1
    assert passenger_bookings[0]["status"] == "cancelled"
    assert client.get(f"/rides/{ride_id}").json()["available_seats"] == 1
