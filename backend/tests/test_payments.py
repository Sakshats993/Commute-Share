from datetime import datetime, timezone
from decimal import Decimal

from app.core.security import create_access_token
from app.models.booking import Booking
from app.models.enums import BookingStatus, PaymentStatus, RideStatus, UserRole
from app.models.payment import Payment
from app.models.ride import Ride
from app.models.user import User
from app.models.vehicle import Vehicle


def auth_headers(user: User) -> dict[str, str]:
    token = create_access_token(subject=user.email)
    return {"Authorization": f"Bearer {token}"}


def test_payment_history_and_earnings_endpoints(client, db):
    driver = User(
        full_name="Driver",
        email="payment-driver@example.com",
        password_hash="test-only-hash",
        role=UserRole.DRIVER,
    )
    passenger = User(
        full_name="Passenger",
        email="payment-passenger@example.com",
        password_hash="test-only-hash",
        role=UserRole.PASSENGER,
    )
    db.add_all([driver, passenger])
    db.flush()

    vehicle = Vehicle(
        owner_id=driver.id,
        make="Test",
        model="Car",
        color="Blue",
        registration_number="PAY-TEST-1",
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
        status=RideStatus.COMPLETED,
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

    payment = Payment(
        ride_id=ride.id,
        booking_id=booking.id,
        amount=Decimal("20.00"),
        status=PaymentStatus.PAID,
    )
    db.add(payment)
    db.commit()

    driver_headers = auth_headers(driver)
    passenger_headers = auth_headers(passenger)

    driver_history = client.get("/payments/driver/history", headers=driver_headers)
    passenger_history = client.get("/payments/passenger/history", headers=passenger_headers)
    earnings = client.get("/payments/driver/earnings", headers=driver_headers)

    assert driver_history.status_code == 200
    assert [item["id"] for item in driver_history.json()] == [payment.id]
    assert passenger_history.status_code == 200
    assert [item["id"] for item in passenger_history.json()] == [payment.id]
    assert earnings.status_code == 200
    assert earnings.json() == {
        "completed_payments": 1,
        "total_earnings": "20.00",
    }
