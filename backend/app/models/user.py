"""
==================================================
CommuteShare User Model

Backend Internship Project
Bermer Software Private Limited

Represents registered users of the platform.

A user can:
- Offer rides
- Book rides
- Register vehicles
- Receive notifications
- Trigger SOS events
- Give and receive ratings
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog
    from app.models.booking import Booking
    from app.models.notification import Notification
    from app.models.rating import Rating
    from app.models.ride import Ride
    from app.models.sos_event import SOSEvent
    from app.models.vehicle import Vehicle
    from app.models.waitlist import Waitlist

class User(BaseModel):
    """
    User model.

    Stores authentication, profile information,
    and relationships to the rest of the system.
    """

    __tablename__ = "users"

    # ======================================================
    # Authentication
    # ======================================================

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # ======================================================
    # Profile
    # ======================================================

    profile_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ======================================================
    # Role & Status
    # ======================================================

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.PASSENGER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    vehicles: Mapped[list["Vehicle"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    rides: Mapped[list["Ride"]] = relationship(
        back_populates="driver",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="passenger",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    ratings_given: Mapped[list["Rating"]] = relationship(
        foreign_keys="Rating.reviewer_id",
        back_populates="reviewer",
        lazy="selectin",
    )

    ratings_received: Mapped[list["Rating"]] = relationship(
        foreign_keys="Rating.reviewee_id",
        back_populates="reviewee",
        lazy="selectin",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    sos_events: Mapped[list["SOSEvent"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    waitlist_entries: Mapped[list["Waitlist"]] = relationship(
        back_populates="passenger",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    average_rating: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    trust_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    completed_rides: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    review_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}')>"
        )