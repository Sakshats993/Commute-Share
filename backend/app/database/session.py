"""
==================================================
CommuteShare Database Session

Backend Internship Project
Bermer Software Private Limited

Creates the SQLAlchemy Engine and Database Session.

Responsibilities:
- Database Engine
- Session Factory
- Dependency Support
==================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# ==========================================================
# Database Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# ==========================================================
# Base Class
# ==========================================================

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass