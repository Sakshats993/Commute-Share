from datetime import datetime, timezone
from decimal import Decimal

import pytest
from fastapi import HTTPException

from app.core.security import create_access_token, create_qr_boarding_token
from app.models.booking import Booking
from app.models.enums import BookingStatus, RideStatus, SOSStatus, UserRole
from app.models.ride import Ride
from app.models.user import User
from app.models.vehicle import Vehicle
from app.services.qr_service import verify_boarding_qr


def _user(db, email, role):
    user = User(full_name=email.split("@")[0], email=email, password_hash="test-hash", role=role)
    db.add(user)
    db.flush()
    return user


def _ride(db, driver, *, status=RideStatus.SCHEDULED):
    vehicle = Vehicle(owner_id=driver.id, make="Test", model="Car", color="Blue",
                      registration_number=f"SAFE-{driver.id}", seating_capacity=4, is_active=True)
    db.add(vehicle)
    db.flush()
    ride = Ride(
        driver_id=driver.id, vehicle_id=vehicle.id,
        pickup_location="Udupi", pickup_latitude=13.34, pickup_longitude=74.74,
        destination_location="Manipal", destination_latitude=13.35, destination_longitude=74.79,
        departure_time=datetime(2030, 1, 1, tzinfo=timezone.utc), total_seats=3,
        available_seats=2, price_per_seat=Decimal("20.00"), status=status,
    )
    db.add(ride)
    db.flush()
    return ride


@pytest.mark.parametrize("booking_status", [BookingStatus.PENDING, BookingStatus.CANCELLED, BookingStatus.WAITLISTED])
def test_qr_rejects_ineligible_booking_statuses(db, booking_status):
    driver = _user(db, "driver@example.com", UserRole.DRIVER)
    passenger = _user(db, "passenger@example.com", UserRole.PASSENGER)
    ride = _ride(db, driver, status=RideStatus.WAITING_FOR_BOARDING)
    booking = Booking(passenger_id=passenger.id, ride_id=ride.id, status=booking_status)
    db.add(booking)
    db.commit()
    token = create_qr_boarding_token(ride_id=ride.id, driver_id=driver.id)

    with pytest.raises(HTTPException) as error:
        verify_boarding_qr(db=db, qr_token=token, passenger_id=passenger.id)

    assert error.value.status_code == 403
    assert booking.has_boarded is False


def test_qr_allows_confirmed_passenger_once(db):
    driver = _user(db, "driver@example.com", UserRole.DRIVER)
    passenger = _user(db, "passenger@example.com", UserRole.PASSENGER)
    ride = _ride(db, driver, status=RideStatus.WAITING_FOR_BOARDING)
    booking = Booking(passenger_id=passenger.id, ride_id=ride.id, status=BookingStatus.CONFIRMED)
    db.add(booking)
    db.commit()
    token = create_qr_boarding_token(ride_id=ride.id, driver_id=driver.id)

    verified_ride = verify_boarding_qr(db=db, qr_token=token, passenger_id=passenger.id)
    assert verified_ride.status == RideStatus.IN_PROGRESS
    assert booking.has_boarded is True
    with pytest.raises(HTTPException) as error:
        verify_boarding_qr(db=db, qr_token=token, passenger_id=passenger.id)
    assert error.value.status_code == 409


def test_starting_ride_enters_boarding_state(client, db):
    driver = _user(db, "driver@example.com", UserRole.DRIVER)
    passenger = _user(db, "passenger@example.com", UserRole.PASSENGER)
    ride = _ride(db, driver)
    db.add(Booking(passenger_id=passenger.id, ride_id=ride.id, status=BookingStatus.CONFIRMED))
    db.commit()
    token = create_access_token(driver.email)

    response = client.patch(f"/rides/{ride.id}/start", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200, response.text
    assert response.json()["status"] == RideStatus.WAITING_FOR_BOARDING.value


def test_cannot_cancel_booking_after_ride_starts(client, db):
    driver = _user(db, "driver@example.com", UserRole.DRIVER)
    passenger = _user(db, "passenger@example.com", UserRole.PASSENGER)
    ride = _ride(db, driver, status=RideStatus.IN_PROGRESS)
    booking = Booking(passenger_id=passenger.id, ride_id=ride.id, status=BookingStatus.CONFIRMED)
    db.add(booking)
    db.commit()
    token = create_access_token(passenger.email)

    response = client.delete(f"/bookings/{booking.id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 409
    assert booking.status == BookingStatus.CONFIRMED
    assert ride.available_seats == 2


def test_sos_rejects_unrelated_or_non_active_ride(client, db):
    driver = _user(db, "driver@example.com", UserRole.DRIVER)
    stranger = _user(db, "stranger@example.com", UserRole.PASSENGER)
    ride = _ride(db, driver, status=RideStatus.SCHEDULED)
    db.commit()
    token = create_access_token(stranger.email)

    response = client.post(
        "/sos/", headers={"Authorization": f"Bearer {token}"},
        json={"ride_id": ride.id, "emergency_type": "Emergency"},
    )

    assert response.status_code == 403


def test_sos_active_ride_notifies_admin_and_supports_triage(client, db):
    driver = _user(db, "driver@example.com", UserRole.DRIVER)
    passenger = _user(db, "passenger@example.com", UserRole.PASSENGER)
    admin = _user(db, "admin@example.com", UserRole.ADMIN)
    ride = _ride(db, driver, status=RideStatus.IN_PROGRESS)
    db.add(Booking(passenger_id=passenger.id, ride_id=ride.id, status=BookingStatus.CONFIRMED))
    db.commit()
    passenger_token = create_access_token(passenger.email)
    admin_token = create_access_token(admin.email)

    created = client.post(
        "/sos/", headers={"Authorization": f"Bearer {passenger_token}"},
        json={"ride_id": ride.id, "emergency_type": "Emergency", "latitude": 13.34, "longitude": 74.74},
    )
    assert created.status_code == 201, created.text
    assert created.json()["status"] == SOSStatus.ACTIVE.value
    assert len(client.get("/notifications/", headers={"Authorization": f"Bearer {admin_token}"}).json()) == 1

    event_id = created.json()["id"]
    acknowledged = client.patch(f"/admin/sos/{event_id}/acknowledge", headers={"Authorization": f"Bearer {admin_token}"})
    assert acknowledged.status_code == 200, acknowledged.text
    assert acknowledged.json()["status"] == SOSStatus.ACKNOWLEDGED.value
    resolved = client.patch(f"/admin/sos/{event_id}/resolve", headers={"Authorization": f"Bearer {admin_token}"})
    assert resolved.status_code == 200, resolved.text
    assert resolved.json()["status"] == SOSStatus.RESOLVED.value


def test_ride_search_applies_filters_and_zero_fare_ceiling(client, db):
    free_driver = _user(db, "free-driver@example.com", UserRole.DRIVER)
    paid_driver = _user(db, "paid-driver@example.com", UserRole.DRIVER)
    free_ride = _ride(db, free_driver)
    paid_ride = _ride(db, paid_driver)
    free_ride.price_per_seat = Decimal("0.00")
    paid_ride.price_per_seat = Decimal("25.00")
    db.commit()

    response = client.get("/rides/search", params={"maximum_price": "0.00", "sort_by": "price"})

    assert response.status_code == 200, response.text
    assert [ride["id"] for ride in response.json()] == [free_ride.id]

