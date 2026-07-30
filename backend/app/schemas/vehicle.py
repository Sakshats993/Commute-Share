"""
==================================================
CommuteShare Vehicle Schemas

Backend Internship Project
Bermer Software Private Limited

Pydantic schemas related to vehicles.

Includes:
- Vehicle Creation
- Vehicle Update
- Vehicle Response
==================================================
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ======================================================
# Base Schema
# ======================================================

class VehicleBase(BaseModel):
    """
    Common vehicle fields.
    """

    make: str = Field(
        ...,
        min_length=2,
        max_length=50,
        examples=["Honda"],
    )

    model: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["City"],
    )

    color: str = Field(
        ...,
        min_length=2,
        max_length=30,
        examples=["White"],
    )

    registration_number: str = Field(
        ...,
        min_length=5,
        max_length=20,
        examples=["KA20AB1234"],
    )

    seating_capacity: int = Field(
        ...,
        ge=1,
        le=10,
        description="Maximum passenger capacity.",
    )


# ======================================================
# Create Vehicle
# ======================================================

class VehicleCreate(VehicleBase):
    """
    Schema used to register a vehicle.
    """

    pass


# ======================================================
# Update Vehicle
# ======================================================

class VehicleUpdate(BaseModel):
    """
    Schema used to update vehicle information.
    """

    make: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    model: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    color: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=30,
    )

    seating_capacity: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
    )

    is_active: Optional[bool] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


# ======================================================
# Vehicle Response
# ======================================================

class VehicleResponse(VehicleBase):
    """
    Vehicle information returned by the API.
    """

    id: int

    owner_id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )