"""
==================================================
CommuteShare SOS Event Model

Backend Internship Project
Bermer Software Private Limited

Represents emergency SOS alerts triggered
by users during a ride.

Features:
- Emergency type
- Ride information
- User location
- Status tracking
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import SOSStatus

if TYPE_CHECKING:
    from app.models.ride import Ride
    from app.models.user import User


class SOSEvent(BaseModel):
    """
    Represents an emergency event triggered
    by a passenger or driver.
    """

    __tablename__ = "sos_events"

    # ======================================================
    # Foreign Keys
    # ======================================================

    user_id: Mapped[int] = mapped_column(
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
    # Emergency Information
    # ======================================================

    emergency_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ======================================================
    # User Location
    # ======================================================

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ======================================================
    # Status
    # ======================================================

    status: Mapped[SOSStatus] = mapped_column(
        Enum(SOSStatus),
        default=SOSStatus.ACTIVE,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    user: Mapped["User"] = relationship(
        back_populates="sos_events",
        lazy="selectin",
    )

    ride: Mapped["Ride"] = relationship(
        back_populates="sos_events",
        lazy="selectin",
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<SOSEvent("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"ride_id={self.ride_id}, "
            f"status='{self.status.value}')>"
        )