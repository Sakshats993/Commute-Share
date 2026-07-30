"""
==================================================
CommuteShare Booking Model

Backend Internship Project
Bermer Software Private Limited

Represents a passenger's booking for a ride.

Features:
- One passenger per booking
- One seat per booking
- Booking status tracking
- Booking cancellation history
==================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

from app.models.base_model import BaseModel
from app.models.enums import BookingStatus

if TYPE_CHECKING:
    from app.models.ride import Ride
    from app.models.user import User


class Booking(BaseModel):
    """
    Represents a passenger's booking for a ride.
    """

    __tablename__ = "bookings"

    # ======================================================
    # Foreign Keys
    # ======================================================

    passenger_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ride_id: Mapped[int] = mapped_column(
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Booking Status
    # ======================================================

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus),
        default=BookingStatus.CONFIRMED,
        nullable=False,
    )

    # ======================================================
    # Cancellation
    # ======================================================

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    passenger: Mapped["User"] = relationship(
        back_populates="bookings",
        lazy="selectin",
    )

    ride: Mapped["Ride"] = relationship(
        back_populates="bookings",
        lazy="selectin",
    )
    
    __table_args__ = (
        UniqueConstraint(
            "passenger_id",
            "ride_id",
            name="uq_booking_passenger_ride",
         ),
    )
    
    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Booking("
            f"id={self.id}, "
            f"passenger_id={self.passenger_id}, "
            f"ride_id={self.ride_id}, "
            f"status='{self.status.value}')>"
        )    