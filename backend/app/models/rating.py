"""
==================================================
CommuteShare Rating Model

Backend Internship Project
Bermer Software Private Limited

Represents ratings and reviews exchanged
between users after completing a ride.

Features:
- 1 to 5 star ratings
- Written review
- One rating per ride
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.ride import Ride
    from app.models.user import User


class Rating(BaseModel):
    """
    Represents a rating given by one user
    to another after completing a ride.
    """

    __tablename__ = "ratings"

    __table_args__ = (
        UniqueConstraint(
            "ride_id",
            "reviewer_id",
            "reviewee_id",
            name="uq_rating_per_ride",
        ),
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="ck_rating_range",
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

    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    reviewee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Rating Information
    # ======================================================

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    review: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    ride: Mapped["Ride"] = relationship(
    back_populates="ratings",
    lazy="selectin",
    )

    reviewer: Mapped["User"] = relationship(
        foreign_keys=[reviewer_id],
        back_populates="ratings_given",
        lazy="selectin",
    )

    reviewee: Mapped["User"] = relationship(
        foreign_keys=[reviewee_id],
        back_populates="ratings_received",
        lazy="selectin",
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Rating("
            f"id={self.id}, "
            f"rating={self.rating}, "
            f"reviewer={self.reviewer_id}, "
            f"reviewee={self.reviewee_id})>"
        )