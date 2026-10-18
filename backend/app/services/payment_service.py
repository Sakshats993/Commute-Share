"""
==================================================
CommuteShare Payment Service

Backend Internship Project
Bermer Software Private Limited

Handles:

- Get Payment
- Get Booking Payment
- Mark Payment Paid
- Mark Payment Failed
==================================================
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import PaymentStatus
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.ride import Ride


# ======================================================
# Get Payment By ID
# ======================================================

def get_payment(
    db: Session,
    payment_id: int,
) -> Payment:
    """
    Return a payment by its ID.
    """

    payment = db.get(
        Payment,
        payment_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )

    return payment


# ======================================================
# Get Booking Payment
# ======================================================

def get_booking_payment(
    db: Session,
    booking_id: int,
) -> Payment:
    """
    Return the payment for a booking.
    """

    payment = db.scalar(
        select(Payment).where(
            Payment.booking_id == booking_id,
        )
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )

    return payment


# ======================================================
# Mark Payment Paid
# ======================================================

def mark_payment_paid(
    db: Session,
    payment: Payment,
    method: str,
) -> Payment:
    """
    Mark a payment as paid.
    """

    if payment.status == PaymentStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment has already been completed.",
        )

    payment.status = PaymentStatus.PAID
    payment.method = method
    payment.paid_at = datetime.now(
        timezone.utc,
    )

    db.commit()

    db.refresh(payment)

    return payment


# ======================================================
# Mark Payment Failed
# ======================================================

def mark_payment_failed(
    db: Session,
    payment: Payment,
) -> Payment:
    """
    Mark a payment as failed.
    """

    if payment.status == PaymentStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Completed payments cannot be marked as failed.",
        )

    payment.status = PaymentStatus.FAILED

    db.commit()

    db.refresh(payment)

    return payment
# ======================================================
# Driver Payment History
# ======================================================

def get_driver_payments(
    db: Session,
    driver_id: int,
) -> list[Payment]:

    stmt = (
        select(Payment)
        .join(Ride)
        .where(Ride.driver_id == driver_id)
        .order_by(Payment.created_at.desc())
    )

    return list(db.scalars(stmt).all())


# ======================================================
# Passenger Payment History
# ======================================================

def get_passenger_payments(
    db: Session,
    passenger_id: int,
) -> list[Payment]:

    stmt = (
        select(Payment)
        .join(Booking)
        .where(Booking.passenger_id == passenger_id)
        .order_by(Payment.created_at.desc())
    )

    return list(db.scalars(stmt).all())


# ======================================================
# Driver Earnings
# ======================================================

def get_driver_earnings(
    db: Session,
    driver_id: int,
):

    stmt = (
        select(Payment)
        .join(Ride)
        .where(
            Ride.driver_id == driver_id,
            Payment.status == PaymentStatus.PAID,
        )
    )

    payments = list(db.scalars(stmt).all())

    total = sum(
        payment.amount
        for payment in payments
    )

    return {
        "completed_payments": len(payments),
        "total_earnings": total,
    }


# ======================================================
# Revenue Statistics
# ======================================================

def get_revenue_statistics(
    db: Session,
):

    stmt = select(Payment).where(
        Payment.status == PaymentStatus.PAID
    )

    payments = list(db.scalars(stmt).all())

    revenue = sum(
        payment.amount
        for payment in payments
    )

    return {
        "paid_payments": len(payments),
        "total_revenue": revenue,
    }
