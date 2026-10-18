"""
==================================================
CommuteShare Base Model

Backend Internship Project
Bermer Software Private Limited

Provides common fields shared by all database
models.

Features:
- Integer Primary Key
- Created Timestamp
- Updated Timestamp
==================================================
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class BaseModel(Base):
    """
    Abstract base model inherited by all database models.
    """

    __abstract__ = True

    # ======================================================
    # Primary Key
    # ======================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # ======================================================
    # Audit Fields
    # ======================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
