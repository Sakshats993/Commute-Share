"""
==================================================
CommuteShare Notification Model

Backend Internship Project
Bermer Software Private Limited

Stores notifications sent to users.

Examples:
- Ride Booking Confirmed
- Ride Cancelled
- Waitlist Promoted
- New Rating Received
- SOS Alert
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum,
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
from app.models.enums import NotificationType

if TYPE_CHECKING:
    from app.models.user import User


class Notification(BaseModel):
    """
    Represents a notification sent to a user.
    """

    __tablename__ = "notifications"

    # ======================================================
    # User
    # ======================================================

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # Notification Content
    # ======================================================

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType),
        nullable=False,
    )

    # ======================================================
    # Status
    # ======================================================

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    user: Mapped["User"] = relationship(
        back_populates="notifications",
        lazy="selectin",
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Notification("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"type='{self.type.value}', "
            f"is_read={self.is_read})>"
        )