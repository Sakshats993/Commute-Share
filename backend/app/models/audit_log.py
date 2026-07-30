"""
==================================================
CommuteShare Audit Log Model

Backend Internship Project
Bermer Software Private Limited

Stores security and system events for auditing.

Examples:
- User Login
- User Registration
- Ride Created
- Ride Updated
- Booking Created
- Booking Cancelled
- SOS Triggered
- Admin Actions
==================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(BaseModel):
    """
    Represents an audit log entry.

    Every important action inside the system
    should create an audit log.
    """

    __tablename__ = "audit_logs"

    # ======================================================
    # User
    # ======================================================

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ======================================================
    # Event Information
    # ======================================================

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ======================================================
    # Request Information
    # ======================================================

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    user: Mapped["User | None"] = relationship(
        back_populates="audit_logs",
        lazy="selectin",
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<AuditLog("
            f"id={self.id}, "
            f"action='{self.action}', "
            f"resource='{self.resource}', "
            f"user_id={self.user_id})>"
        )