"""
==================================================
CommuteShare User Service

Backend Internship Project
Bermer Software Private Limited

Handles:
- User Retrieval
- Profile Updates
- Account Deactivation
==================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserUpdate


# ==========================================================
# Get User By ID
# ==========================================================

def get_user_by_id(
    db: Session,
    *,
    user_id: int,
) -> User:
    """
    Return a user by ID.
    """

    stmt = select(User).where(
        User.id == user_id
    )

    user = db.scalar(stmt)

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


# ==========================================================
# Get User By Email
# ==========================================================

def get_user_by_email(
    db: Session,
    *,
    email: str,
) -> User | None:
    """
    Return a user by email.
    """

    stmt = select(User).where(
        User.email == email
    )

    return db.scalar(stmt)


# ==========================================================
# Update User Profile
# ==========================================================

def update_user_profile(
    db: Session,
    *,
    current_user: User,
    user_data: UserUpdate,
) -> User:
    """
    Update current user's profile.
    """

    update_data = user_data.model_dump(
        exclude_unset=True,
    )

    # Prevent email duplication
    if "email" in update_data:

        existing = get_user_by_email(
            db=db,
            email=update_data["email"],
        )

        if (
            existing is not None
            and existing.id != current_user.id
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

    for field, value in update_data.items():

        setattr(
            current_user,
            field,
            value,
        )

    try:

        db.commit()

        db.refresh(current_user)

    except Exception:

        db.rollback()

        raise

    return current_user


# ==========================================================
# Deactivate User
# ==========================================================

def deactivate_user(
    db: Session,
    *,
    current_user: User,
) -> User:
    """
    Deactivate a user account.
    """

    if not current_user.is_active:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is already deactivated.",
        )

    current_user.is_active = False

    try:

        db.commit()

        db.refresh(current_user)

    except Exception:

        db.rollback()

        raise

    return current_user


# ==========================================================
# Reactivate User
# ==========================================================

def reactivate_user(
    db: Session,
    *,
    user: User,
) -> User:
    """
    Reactivate a user account.
    """

    user.is_active = True

    try:

        db.commit()

        db.refresh(user)

    except Exception:

        db.rollback()

        raise

    return user