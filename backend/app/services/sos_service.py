"""
==================================================
CommuteShare SOS Service

Backend Internship Project
Bermer Software Private Limited

Handles:
- Create SOS Event
- Retrieve SOS Events
- View SOS History
==================================================
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sos_event import SOSEvent
from app.models.user import User

from app.schemas.misc import SOSCreate


# ==========================================================
# Get SOS By ID
# ==========================================================

def get_sos_by_id(
    db: Session,
    *,
    sos_id: int,
) -> SOSEvent:
    """
    Return an SOS event by ID.
    """

    stmt = select(SOSEvent).where(
        SOSEvent.id == sos_id,
    )

    sos_event = db.scalar(stmt)

    if sos_event is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SOS event not found.",
        )

    return sos_event


# ==========================================================
# User SOS History
# ==========================================================

def get_user_sos_events(
    db: Session,
    *,
    user_id: int,
) -> list[SOSEvent]:
    """
    Return all SOS events
    for a user.
    """

    stmt = (
        select(SOSEvent)
        .where(
            SOSEvent.user_id == user_id,
        )
        .order_by(
            SOSEvent.created_at.desc(),
        )
    )

    return list(
        db.scalars(stmt).all()
    )


# ==========================================================
# Create SOS Event
# ==========================================================

def create_sos_event(
    db: Session,
    *,
    user: User,
    sos_data: SOSCreate,
) -> SOSEvent:
    """
    Create a new SOS event.
    """

    sos_event = SOSEvent(
        user_id=user.id,
        **sos_data.model_dump(),
    )

    try:

        db.add(sos_event)

        db.commit()

        db.refresh(sos_event)

    except Exception:

        db.rollback()

        raise

    return sos_event


# ==========================================================
# Delete SOS Event
# ==========================================================

def delete_sos_event(
    db: Session,
    *,
    sos_id: int,
    user: User,
) -> None:
    """
    Delete an SOS event.

    Users may only delete
    their own SOS events.
    """

    sos_event = get_sos_by_id(
        db=db,
        sos_id=sos_id,
    )

    if sos_event.user_id != user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this SOS event.",
        )

    try:

        db.delete(sos_event)

        db.commit()

    except Exception:

        db.rollback()

        raise