"""
==================================================
CommuteShare Ride Model

Backend Internship Project
Bermer Software Private Limited

Represents rides created by drivers.

A ride contains:
- Driver information
- Vehicle information
- Route details
- Seat availability
- Pricing
- Ride status
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
    Text,
    Float,
    Integer,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import RideStatus


if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.user import User
    from app.models.vehicle import Vehicle
    from app.models.waitlist import Waitlist
    from app.models.rating import Rating
    from app.models.sos_event import SOSEvent
    from app.models.payment import Payment

class Ride(BaseModel):
    """
    Represents a ride offered by a driver.
    """

    __tablename__ = "rides"

    # ======================================================
    # Driver & Vehicle
    # ======================================================

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Pickup Information
    # ======================================================

    pickup_location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    pickup_latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    pickup_longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ======================================================
    # Destination Information
    # ======================================================

    destination_location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    destination_latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    destination_longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ======================================================
    # Schedule
    # ======================================================

    departure_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    estimated_arrival_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

        # ======================================================
    # Ride Lifecycle
    # ======================================================

    boarding_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    driver_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    passenger_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ======================================================
    # Capacity
    # ======================================================

    total_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    available_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # ======================================================
    # Pricing
    # ======================================================

    price_per_seat: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # ======================================================
    # Additional Information
    # ======================================================

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ======================================================
    # Ride Status
    # ======================================================

    status: Mapped[RideStatus] = mapped_column(
        Enum(RideStatus),
        default=RideStatus.SCHEDULED,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    driver: Mapped["User"] = relationship(
        back_populates="rides",
        lazy="selectin",
    )

    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="rides",
        lazy="selectin",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="ride",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    waitlist: Mapped[list["Waitlist"]] = relationship(
        back_populates="ride",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    ratings: Mapped[list["Rating"]] = relationship(
    back_populates="ride",
    cascade="all, delete-orphan",
    lazy="selectin",
    )
    
    sos_events: Mapped[list["SOSEvent"]] = relationship(
    back_populates="ride",
    cascade="all, delete-orphan",
    lazy="selectin",
    )
    payments: Mapped[list["Payment"]] = relationship(
    back_populates="ride",
    cascade="all, delete-orphan",
    lazy="selectin",
    )
    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Ride("
            f"id={self.id}, "
            f"driver_id={self.driver_id}, "
            f"pickup='{self.pickup_location}', "
            f"destination='{self.destination_location}', "
            f"status='{self.status.value}')>"
        )
