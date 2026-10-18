from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token, create_refresh_token
from app.database.session import Base
from app.models.booking import Booking
from app.models.enums import BookingStatus, PaymentStatus, RideStatus, UserRole
from app.models.payment import Payment
from app.models.ride import Ride
from app.models.rating import Rating
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.waitlist import Waitlist
from app.services.booking_service import cancel_booking, confirm_booking
from app.services.ride_service import end_ride


def make_user(db, email: str, role: UserRole) -> User:
    user = User(
        full_name=email.split("@")[0],
        email=email,
        password_hash="test-only-hash",
        role=role,
    )
    db.add(user)
    db.flush()
    return user


def auth_headers(user: User) -> dict[str, str]:
    token = create_access_token(subject=user.email)
    return {"Authorization": f"Bearer {token}"}


def make_ride_and_booking(db, driver: User, passenger: User):
    vehicle = Vehicle(
        owner_id=driver.id,
        make="Test",
        model="Car",
        color="Blue",
        registration_number=f"TEST-{driver.id}-{passenger.id}",
        seating_capacity=4,
        is_active=True,
    )
    db.add(vehicle)
    db.flush()

    ride = Ride(
        driver_id=driver.id,
        vehicle_id=vehicle.id,
        pickup_location="Udupi",
        pickup_latitude=13.34,
        pickup_longitude=74.74,
        destination_location="Manipal",
        destination_latitude=13.35,
        destination_longitude=74.79,
        departure_time=datetime(2030, 1, 1, tzinfo=timezone.utc),
        total_seats=3,
        available_seats=2,
        price_per_seat=Decimal("20.00"),
        status=RideStatus.SCHEDULED,
    )
    db.add(ride)
    db.flush()

    booking = Booking(
        passenger_id=passenger.id,
        ride_id=ride.id,
        status=BookingStatus.CONFIRMED,
    )
    db.add(booking)
    db.flush()
    return ride, booking


def test_user_cannot_cancel_another_users_booking(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    stranger = make_user(db, "stranger@example.com", UserRole.PASSENGER)
    _, booking = make_ride_and_booking(db, driver, passenger)
    db.commit()

    response = client.delete(
        f"/bookings/{booking.id}",
        headers=auth_headers(stranger),
    )

    assert response.status_code == 403
    db.refresh(booking)
    assert booking.status == BookingStatus.CONFIRMED


@pytest.mark.parametrize("role", [UserRole.DRIVER, UserRole.ADMIN])
def test_only_passengers_can_create_bookings(client, db, role):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    account = make_user(db, f"booking-{role.value}@example.com", role)
    ride, _ = make_ride_and_booking(db, driver, passenger)
    db.commit()

    response = client.post(
        "/bookings",
        json={"ride_id": ride.id},
        headers=auth_headers(account),
    )

    assert response.status_code == 403
    assert db.query(Booking).filter(
        Booking.ride_id == ride.id,
        Booking.passenger_id == account.id,
    ).count() == 0


def test_ride_completion_failure_rolls_back_without_printing_error(db, monkeypatch, capsys):
    driver = make_user(db, "ride-error-driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "ride-error-passenger@example.com", UserRole.PASSENGER)
    ride, _ = make_ride_and_booking(db, driver, passenger)
    ride.status = RideStatus.IN_PROGRESS
    db.commit()
    original_rollback = db.rollback

    def fail_commit():
        raise RuntimeError("database detail should not be printed")

    monkeypatch.setattr(db, "commit", fail_commit)
    monkeypatch.setattr(db, "rollback", original_rollback)

    with pytest.raises(RuntimeError, match="database detail"):
        end_ride(db, ride=ride, driver=driver)

    db.refresh(ride)
    assert ride.status == RideStatus.IN_PROGRESS
    assert capsys.readouterr().out == ""


def test_deactivated_user_cannot_submit_or_list_ratings(client, db):
    driver = make_user(db, "inactive-rating-driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "inactive-rating-passenger@example.com", UserRole.PASSENGER)
    ride, booking = make_ride_and_booking(db, driver, passenger)
    ride.status = RideStatus.COMPLETED
    rating = Rating(
        ride_id=ride.id,
        reviewer_id=passenger.id,
        reviewee_id=driver.id,
        rating=4,
        review="Existing review",
    )
    db.add(rating)
    passenger.is_active = False
    db.commit()

    create_response = client.post(
        "/ratings",
        json={"booking_id": booking.id, "rating": 5},
        headers=auth_headers(passenger),
    )
    list_response = client.get("/ratings/me", headers=auth_headers(passenger))
    candidates_response = client.get(
        "/ratings/candidates", headers=auth_headers(passenger)
    )
    update_response = client.put(
        f"/ratings/{rating.id}",
        json={"rating": 1},
        headers=auth_headers(passenger),
    )
    delete_response = client.delete(
        f"/ratings/{rating.id}", headers=auth_headers(passenger)
    )

    assert create_response.status_code == 403
    assert list_response.status_code == 403
    assert candidates_response.status_code == 403
    assert update_response.status_code == 403
    assert delete_response.status_code == 403
    assert db.query(Rating).filter_by(ride_id=ride.id).count() == 1


def test_refresh_token_cannot_access_protected_endpoints(client, db):
    user = make_user(db, "token-user@example.com", UserRole.PASSENGER)
    db.commit()

    access_response = client.get("/auth/me", headers=auth_headers(user))
    refresh_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {create_refresh_token(user.email)}"
        },
    )

    assert access_response.status_code == 200
    assert refresh_response.status_code == 401


@pytest.mark.parametrize(
    ("method", "path", "payload"),
    [
        ("put", "/rides/{ride_id}", {"notes": "changed by stranger"}),
        ("delete", "/rides/{ride_id}", None),
    ],
)
def test_driver_cannot_modify_an_unrelated_ride(
    client, db, method, path, payload
):
    owner = make_user(db, "owner@example.com", UserRole.DRIVER)
    other_driver = make_user(db, "other-driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "rider@example.com", UserRole.PASSENGER)
    ride, _ = make_ride_and_booking(db, owner, passenger)
    db.commit()

    request_path = path.format(ride_id=ride.id)
    if method == "delete":
        response = client.delete(
            request_path,
            headers=auth_headers(other_driver),
        )
    else:
        response = client.put(
            request_path,
            json=payload,
            headers=auth_headers(other_driver),
        )

    assert response.status_code == 403
    db.refresh(ride)
    assert ride.driver_id == owner.id
    assert ride.notes is None


def test_passenger_cannot_access_admin_operations(client, db):
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    db.commit()

    response = client.get(
        "/admin/users",
        headers=auth_headers(passenger),
    )

    assert response.status_code == 403


def test_public_user_profile_requires_auth_and_hides_contact_details(client, db):
    profile_owner = make_user(db, "profile@example.com", UserRole.PASSENGER)
    profile_owner.phone_number = "+1-555-0100"
    viewer = make_user(db, "viewer@example.com", UserRole.PASSENGER)
    db.commit()

    anonymous_response = client.get(f"/users/{profile_owner.id}")
    profile_response = client.get(
        f"/users/{profile_owner.id}", headers=auth_headers(viewer)
    )

    assert anonymous_response.status_code == 401
    assert profile_response.status_code == 200
    assert "email" not in profile_response.json()
    assert "phone_number" not in profile_response.json()


def test_payment_access_is_limited_to_participants_and_admin(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    stranger = make_user(db, "stranger@example.com", UserRole.PASSENGER)
    admin = make_user(db, "admin@example.com", UserRole.ADMIN)
    ride, booking = make_ride_and_booking(db, driver, passenger)
    payment = Payment(
        ride_id=ride.id,
        booking_id=booking.id,
        amount=Decimal("20.00"),
        status=PaymentStatus.UNPAID,
    )
    db.add(payment)
    db.commit()

    payment_response = client.get(
        f"/payments/{payment.id}",
        headers=auth_headers(stranger),
    )
    booking_payment_response = client.get(
        f"/payments/booking/{booking.id}",
        headers=auth_headers(stranger),
    )
    participant_response = client.get(
        f"/payments/{payment.id}",
        headers=auth_headers(passenger),
    )
    admin_response = client.get(
        f"/payments/{payment.id}",
        headers=auth_headers(admin),
    )

    assert payment_response.status_code == 403
    assert booking_payment_response.status_code == 403
    assert participant_response.status_code == 200
    assert admin_response.status_code == 200


@pytest.mark.parametrize("action", ["paid", "failed"])
def test_payment_status_changes_are_admin_only(client, db, action):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    ride, booking = make_ride_and_booking(db, driver, passenger)
    payment = Payment(
        ride_id=ride.id,
        booking_id=booking.id,
        amount=Decimal("20.00"),
        status=PaymentStatus.UNPAID,
    )
    db.add(payment)
    db.commit()

    response = client.patch(
        f"/payments/{payment.id}/{action}",
        json={"method": "manual"} if action == "paid" else None,
        headers=auth_headers(passenger),
    )

    assert response.status_code == 403
    db.refresh(payment)
    assert payment.status == PaymentStatus.UNPAID


def test_confirmations_do_not_exceed_last_available_seat(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    first_passenger = make_user(db, "first@example.com", UserRole.PASSENGER)
    second_passenger = make_user(db, "second@example.com", UserRole.PASSENGER)
    ride, first_booking = make_ride_and_booking(db, driver, first_passenger)
    ride.available_seats = 1
    first_booking.status = BookingStatus.PENDING
    second_booking = Booking(
        passenger_id=second_passenger.id,
        ride_id=ride.id,
        status=BookingStatus.PENDING,
    )
    db.add(second_booking)
    db.commit()

    first_response = client.patch(
        f"/bookings/{first_booking.id}/confirm",
        headers=auth_headers(driver),
    )
    second_response = client.patch(
        f"/bookings/{second_booking.id}/confirm",
        headers=auth_headers(driver),
    )

    assert first_response.status_code == 200
    assert second_response.status_code in (400, 409)
    db.refresh(ride)
    assert ride.available_seats == 0
    assert (
        db.query(Booking)
        .filter(
            Booking.ride_id == ride.id,
            Booking.status == BookingStatus.CONFIRMED,
        )
        .count()
        == 1
    )


def test_cancellation_promotes_waitlist_in_same_transaction(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    queued_passenger = make_user(db, "queued@example.com", UserRole.PASSENGER)
    ride, booking = make_ride_and_booking(db, driver, passenger)
    ride.available_seats = 0
    waitlist = Waitlist(
        ride_id=ride.id,
        passenger_id=queued_passenger.id,
        queue_position=1,
    )
    db.add(waitlist)
    db.commit()

    response = client.delete(
        f"/bookings/{booking.id}",
        headers=auth_headers(passenger),
    )

    assert response.status_code == 204
    db.refresh(ride)
    db.refresh(booking)
    promoted = (
        db.query(Booking)
        .filter(
            Booking.ride_id == ride.id,
            Booking.passenger_id == queued_passenger.id,
        )
        .one()
    )
    assert booking.status == BookingStatus.CANCELLED
    assert promoted.status == BookingStatus.CONFIRMED
    assert ride.available_seats == 0
    assert db.query(Waitlist).filter(Waitlist.ride_id == ride.id).count() == 0


def test_cancellation_failure_rolls_back_booking_and_seat_changes(db, monkeypatch):
    import app.services.booking_service as booking_service

    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    queued_passenger = make_user(db, "queued@example.com", UserRole.PASSENGER)
    ride, booking = make_ride_and_booking(db, driver, passenger)
    ride.available_seats = 0
    waitlist = Waitlist(
        ride_id=ride.id,
        passenger_id=queued_passenger.id,
        queue_position=1,
    )
    db.add(waitlist)
    db.commit()

    def fail_notification(**kwargs):
        raise RuntimeError("notification storage unavailable")

    monkeypatch.setattr(booking_service, "create_notification", fail_notification)

    with pytest.raises(RuntimeError, match="notification storage unavailable"):
        cancel_booking(db, booking=booking)

    db.refresh(ride)
    db.refresh(booking)
    assert booking.status == BookingStatus.CONFIRMED
    assert ride.available_seats == 0
    assert db.query(Waitlist).filter(Waitlist.ride_id == ride.id).count() == 1


def test_duplicate_booking_request_is_rejected(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    ride, _ = make_ride_and_booking(db, driver, passenger)
    db.commit()

    response = client.post(
        "/bookings",
        json={"ride_id": ride.id},
        headers=auth_headers(passenger),
    )

    assert response.status_code == 400


def test_cancelled_booking_can_be_reused_for_rebooking(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    passenger = make_user(db, "passenger@example.com", UserRole.PASSENGER)
    ride, booking = make_ride_and_booking(db, driver, passenger)
    booking.status = BookingStatus.CANCELLED
    db.commit()

    response = client.post(
        "/bookings",
        json={"ride_id": ride.id},
        headers=auth_headers(passenger),
    )

    assert response.status_code == 201
    bookings = db.query(Booking).filter(Booking.ride_id == ride.id).all()
    assert len(bookings) == 1
    assert bookings[0].status == BookingStatus.PENDING
    assert bookings[0].cancelled_at is None


def test_full_ride_request_returns_waitlist_response(client, db):
    driver = make_user(db, "driver@example.com", UserRole.DRIVER)
    existing_passenger = make_user(db, "existing@example.com", UserRole.PASSENGER)
    new_passenger = make_user(db, "new@example.com", UserRole.PASSENGER)
    ride, _ = make_ride_and_booking(db, driver, existing_passenger)
    ride.available_seats = 0
    db.commit()

    response = client.post(
        "/bookings",
        json={"ride_id": ride.id},
        headers=auth_headers(new_passenger),
    )

    assert response.status_code == 201
    assert response.json()["queue_position"] == 1


@pytest.mark.skipif(
    not os.getenv("COMMUTESHARE_TEST_POSTGRES_URL"),
    reason="requires an isolated PostgreSQL test database",
)
def test_parallel_confirmations_cannot_overbook_last_seat():
    engine = create_engine(os.environ["COMMUTESHARE_TEST_POSTGRES_URL"])
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)

    try:
        with TestSession() as db:
            driver = make_user(db, "race-driver@example.com", UserRole.DRIVER)
            first_passenger = make_user(db, "race-first@example.com", UserRole.PASSENGER)
            second_passenger = make_user(db, "race-second@example.com", UserRole.PASSENGER)
            ride, first_booking = make_ride_and_booking(db, driver, first_passenger)
            ride.available_seats = 1
            first_booking.status = BookingStatus.PENDING
            second_booking = Booking(
                passenger_id=second_passenger.id,
                ride_id=ride.id,
                status=BookingStatus.PENDING,
            )
            db.add(second_booking)
            db.commit()
            ride_id = ride.id
            booking_ids = [first_booking.id, second_booking.id]
            driver_id = driver.id

        start_together = threading.Barrier(2)

        def confirm(booking_id: int) -> bool:
            with TestSession() as db:
                booking = db.get(Booking, booking_id)
                driver = db.get(User, driver_id)
                start_together.wait(timeout=10)
                try:
                    confirm_booking(db, booking=booking, driver=driver)
                    return True
                except HTTPException as error:
                    assert error.status_code in (400, 409)
                    return False

        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(confirm, booking_ids))

        assert sum(outcomes) == 1
        with TestSession() as db:
            ride = db.get(Ride, ride_id)
            confirmed_count = (
                db.query(Booking)
                .filter(
                    Booking.ride_id == ride_id,
                    Booking.status == BookingStatus.CONFIRMED,
                )
                .count()
            )
            assert ride.available_seats == 0
            assert confirmed_count == 1
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
