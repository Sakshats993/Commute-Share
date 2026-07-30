"""
==================================================
CommuteShare SOS Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- Trigger SOS
- View Personal SOS History
- View SOS Details
==================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_active_user,
    get_db,
)

from app.models.user import User

from app.schemas.misc import (
    SOSCreate,
    SOSResponse,
)

from app.services.sos_service import (
    create_sos_event,
    get_sos_by_id,
    get_user_sos_events,
)

router = APIRouter(
    prefix="/sos",
    tags=["SOS"],
)
# ==========================================================
# Trigger SOS
# ==========================================================

@router.post(
    "/",
    response_model=SOSResponse,
    status_code=status.HTTP_201_CREATED,
)
def trigger_sos(
    sos_data: SOSCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Trigger an SOS event.
    """

    return create_sos_event(
        db=db,
        user=current_user,
        sos_data=sos_data,
    )
# ==========================================================
# My SOS History
# ==========================================================

@router.get(
    "/me",
    response_model=list[SOSResponse],
)
def get_my_sos_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return current user's SOS history.
    """

    return get_user_sos_events(
        db=db,
        user_id=current_user.id,
    )
# ==========================================================
# SOS Details
# ==========================================================

@router.get(
    "/{sos_id}",
    response_model=SOSResponse,
)
def get_sos(
    sos_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Return SOS event details.
    """

    sos_event = get_sos_by_id(
        db=db,
        sos_id=sos_id,
    )

    if sos_event.user_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

    return sos_event