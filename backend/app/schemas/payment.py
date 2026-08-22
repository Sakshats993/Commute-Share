"""
==================================================
CommuteShare Payment Schemas

Backend Internship Project
Bermer Software Private Limited

Schemas used for payment responses and updates.
==================================================
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import PaymentStatus


# ======================================================
# Payment Response
# ======================================================

class PaymentResponse(BaseModel):
    """
    Payment information returned by the API.
    """

    id: int

    ride_id: int

    booking_id: int

    amount: Decimal

    status: PaymentStatus

    method: str | None

    paid_at: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ======================================================
# Mark Payment Paid
# ======================================================

class PaymentUpdate(BaseModel):
    """
    Update payment information.
    """

    method: str

class EarningsResponse(BaseModel):
    completed_payments: int
    total_earnings: Decimal


class RevenueResponse(BaseModel):
    paid_payments: int
    total_revenue: Decimal