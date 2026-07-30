"""
==================================================
CommuteShare Reputation Service

Backend Internship Project
Bermer Software Private Limited

Handles reputation and trust score calculations.

Calculates:
- Average Rating
- Trust Score
- Completion Rate
- Cancellation Rate
==================================================
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.rating import Rating
from app.models.user import User


# ======================================================
# Average Rating
# ======================================================

def calculate_average_rating(
    db: Session,
    *,
    user_id: int,
) -> float:
    """
    Calculate a user's average rating.
    """

    stmt = (
        select(func.avg(Rating.rating))
        .where(Rating.reviewee_id == user_id)
    )

    average = db.scalar(stmt)

    if average is None:
        return 0.0

    return round(float(average), 2)


# ======================================================
# Completion Rate
# ======================================================

def calculate_completion_rate(
    user: User,
) -> float:
    """
    Calculate ride completion percentage.
    """

    total = (
        user.completed_rides +
        user.cancelled_rides
    )

    if total == 0:
        return 100.0

    return round(
        (user.completed_rides / total) * 100,
        2,
    )


# ======================================================
# Cancellation Rate
# ======================================================

def calculate_cancellation_rate(
    user: User,
) -> float:
    """
    Calculate cancellation percentage.
    """

    total = (
        user.completed_rides +
        user.cancelled_rides
    )

    if total == 0:
        return 0.0

    return round(
        (user.cancelled_rides / total) * 100,
        2,
    )


# ======================================================
# Trust Score
# ======================================================

def calculate_trust_score(
    db: Session,
    *,
    user: User,
) -> float:
    """
    Calculate an overall trust score.

    Formula:

    50% Rating
    30% Completion Rate
    20% Verification
    """

    average_rating = calculate_average_rating(
        db,
        user_id=user.id,
    )

    completion_rate = calculate_completion_rate(
        user,
    )

    verification_bonus = (
        100
        if user.is_verified
        else 0
    )

    trust_score = (
        (average_rating / 5) * 50
        + (completion_rate / 100) * 30
        + (verification_bonus / 100) * 20
    )

    return round(trust_score, 2)


# ======================================================
# Refresh Reputation
# ======================================================

def refresh_user_reputation(
    db: Session,
    *,
    user: User,
) -> User:
    """
    Update user's stored reputation values.
    """

    user.average_rating = calculate_average_rating(
        db,
        user_id=user.id,
    )

    user.trust_score = calculate_trust_score(
        db,
        user=user,
    )

    try:

        db.commit()

        db.refresh(user)

    except Exception:

        db.rollback()

        raise

    return user