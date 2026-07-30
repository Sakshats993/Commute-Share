"""
==================================================
CommuteShare Dependencies

Backend Internship Project
Bermer Software Private Limited

This module contains reusable FastAPI dependencies
used throughout the application.

Responsibilities:
- Database Session
- Current User Authentication
- Active User Validation
- Driver Authorization
- Admin Authorization
==================================================
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import get_token_subject
from app.database.session import SessionLocal
from app.models.user import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ==========================================================
# Database Dependency
# ==========================================================

def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Returns the currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        subject = get_token_subject(token)

    except JWTError:
        raise credentials_exception
    stmt = select(User).where(User.email == subject)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


# ==========================================================
# Active User
# ==========================================================

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Returns only active users.
    """

    if not current_user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    return current_user


# ==========================================================
# Driver Authorization
# ==========================================================

def require_driver(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allows only drivers.
    """

    if current_user.role != "driver":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver privileges required.",
        )

    return current_user


# ==========================================================
# Passenger Authorization
# ==========================================================

def require_passenger(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allows only passengers.
    """

    if current_user.role != "passenger":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Passenger privileges required.",
        )

    return current_user


# ==========================================================
# Admin Authorization
# ==========================================================

def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allows only administrators.
    """

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user