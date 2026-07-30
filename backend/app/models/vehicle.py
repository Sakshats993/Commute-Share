"""
==================================================
CommuteShare Vehicle Model

Backend Internship Project
Bermer Software Private Limited

Represents vehicles owned by users that can be
used to offer rides.
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.ride import Ride
    from app.models.user import User


class Vehicle(BaseModel):
    """
    Vehicle model.

    Stores information about vehicles registered
    by users.
    """

    __tablename__ = "vehicles"

    # ======================================================
    # Owner
    # ======================================================

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Vehicle Information
    # ======================================================

    make: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    registration_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    seating_capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    owner: Mapped["User"] = relationship(
        back_populates="vehicles",
    )

    rides: Mapped[list["Ride"]] = relationship(
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Vehicle(id={self.id}, "
            f"registration='{self.registration_number}')>"
        )