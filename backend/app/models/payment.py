"""
==================================================
CommuteShare Payment Model

Backend Internship Project
Bermer Software Private Limited

Represents a payment for a completed booking.

A payment is created automatically after a ride
is successfully completed and confirmed.

Features:
- One payment per booking
- Linked to a ride
- Payment status tracking
- Payment method
==================================================
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import PaymentStatus

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.ride import Ride


class Payment(BaseModel):
    """
    Represents payment for a booking.
    """

    __tablename__ = "payments"

    __table_args__ = (
        UniqueConstraint(
            "booking_id",
            name="uq_payment_booking",
        ),
    )

    # ======================================================
    # Foreign Keys
    # ======================================================

    ride_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rides.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    booking_id: Mapped[int] = mapped_column(
        ForeignKey(
            "bookings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Payment Information
    # ======================================================

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.UNPAID,
        nullable=False,
    )

    method: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    ride: Mapped["Ride"] = relationship(
        back_populates="payments",
        lazy="selectin",
    )

    booking: Mapped["Booking"] = relationship(
        back_populates="payment",
        lazy="selectin",
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Payment("
            f"id={self.id}, "
            f"booking_id={self.booking_id}, "
            f"amount={self.amount}, "
            f"status='{self.status.value}')>"
        )