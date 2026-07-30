"""
==================================================
CommuteShare Waitlist Model

Backend Internship Project
Bermer Software Private Limited

Represents passengers waiting for a seat
when a ride has reached full capacity.
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.ride import Ride
    from app.models.user import User


class Waitlist(BaseModel):
    """
    Represents a passenger waiting for a seat
    on a full ride.
    """

    __tablename__ = "waitlists"

    __table_args__ = (
        UniqueConstraint(
            "ride_id",
            "passenger_id",
            name="uq_waitlist_passenger_ride",
        ),
    )

    # ======================================================
    # Foreign Keys
    # ======================================================

    ride_id: Mapped[int] = mapped_column(
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    passenger_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Queue Position
    # ======================================================

    queue_position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    ride: Mapped["Ride"] = relationship(
        back_populates="waitlist",
        lazy="selectin",
    )
    
    passenger: Mapped["User"] = relationship(
    back_populates="waitlist_entries",
    lazy="selectin",
    )
    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Waitlist("
            f"id={self.id}, "
            f"ride_id={self.ride_id}, "
            f"passenger_id={self.passenger_id}, "
            f"position={self.queue_position})>"
        )