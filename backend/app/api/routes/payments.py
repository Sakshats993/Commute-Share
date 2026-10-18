"""
==================================================
CommuteShare Payment Routes

Backend Internship Project
Bermer Software Private Limited

Handles:

- View Payment
- View Booking Payment
- Mark Payment Paid
- Mark Payment Failed
==================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.core.deps import (
    get_db,
    get_current_active_user,
    require_admin,
)

from app.models.enums import UserRole
from app.models.user import User

from app.schemas.payment import (
    PaymentResponse,
    PaymentUpdate,
    EarningsResponse,
    RevenueResponse,
)

from app.services.payment_service import (
    get_payment,
    get_booking_payment,
    mark_payment_paid,
    mark_payment_failed,
    get_driver_payments,
    get_passenger_payments,
    get_driver_earnings,
    get_revenue_statistics,
)
from app.core.deps import require_driver, require_passenger

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


def ensure_payment_access(payment, current_user: User) -> None:
    """Allow payment reads only to a participant or an administrator."""
    if current_user.role == UserRole.ADMIN:
        return

    is_passenger = payment.booking.passenger_id == current_user.id
    is_driver = payment.ride.driver_id == current_user.id
    if not (is_passenger or is_driver):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this payment.",
        )


# ======================================================
# Get Payment
# ======================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment_route(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    ),
):
    payment = get_payment(
        db=db,
        payment_id=payment_id,
    )
    ensure_payment_access(payment, current_user)

    return payment


# ======================================================
# Get Booking Payment
# ======================================================

@router.get(
    "/booking/{booking_id}",
    response_model=PaymentResponse,
)
def get_booking_payment_route(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    ),
):
    payment = get_booking_payment(
        db=db,
        booking_id=booking_id,
    )
    ensure_payment_access(payment, current_user)

    return payment


# ======================================================
# Mark Payment Paid
# ======================================================

@router.patch(
    "/{payment_id}/paid",
    response_model=PaymentResponse,
)
def mark_paid_route(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    payment = get_payment(
        db=db,
        payment_id=payment_id,
    )

    return mark_payment_paid(
        db=db,
        payment=payment,
        method=payment_data.method,
    )


# ======================================================
# Mark Payment Failed
# ======================================================

@router.patch(
    "/{payment_id}/failed",
    response_model=PaymentResponse,
)
def mark_failed_route(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    payment = get_payment(
        db=db,
        payment_id=payment_id,
    )

    return mark_payment_failed(
        db=db,
        payment=payment,
    )
@router.get(
    "/driver/history",
    response_model=list[PaymentResponse],
)
def driver_payment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    return get_driver_payments(
        db=db,
        driver_id=current_user.id,
    )
@router.get(
    "/passenger/history",
    response_model=list[PaymentResponse],
)
def passenger_payment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_passenger),
):
    return get_passenger_payments(
        db=db,
        passenger_id=current_user.id,
    )
@router.get(
    "/driver/earnings",
    response_model=EarningsResponse,
)
def driver_earnings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver),
):
    return get_driver_earnings(
        db=db,
        driver_id=current_user.id,
    )
@router.get(
    "/admin/revenue",
    response_model=RevenueResponse,
)
def revenue_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_revenue_statistics(
        db=db,
    )
