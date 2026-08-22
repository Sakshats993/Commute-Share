"""
==================================================
Rating Routes
==================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.rating import Rating
from app.models.user import User
from app.schemas.misc import (
    RatingCreate,
    RatingResponse,
    RatingUpdate,
    RatingCandidateResponse,
)
from app.services.rating_service import (
    create_rating,
    delete_rating,
    get_rating_candidates,
    get_user_ratings,
    update_rating,
)

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)


# =====================================================
# Create Rating
# =====================================================

@router.post(
    "/",
    response_model=RatingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rating_route(
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_rating(
        db=db,
        rating_data=rating_data,
        reviewer=current_user,
    )

@router.get(
    "/me",
    response_model=list[RatingResponse],
)
def get_my_ratings_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_ratings(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/candidates",
    response_model=list[RatingCandidateResponse],
)
def get_rating_candidates_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_rating_candidates(
        db=db,
        current_user=current_user,
    )
# =====================================================
# Get My Ratings
# =====================================================

@router.get(
    "/me",
    response_model=list[RatingResponse],
)
def get_my_ratings_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_ratings(
        db=db,
        user_id=current_user.id,
    )
# =====================================================
# Get Ratings for User
# =====================================================

@router.get(
    "/user/{user_id}",
    response_model=list[RatingResponse],
)
def get_user_ratings_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_ratings(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Update Rating
# =====================================================

@router.put(
    "/{rating_id}",
    response_model=RatingResponse,
)
def update_rating_route(
    rating_id: int,
    rating_data: RatingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rating = db.get(Rating, rating_id)

    if not rating:
        raise HTTPException(
            status_code=404,
            detail="Rating not found.",
        )

    if rating.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this rating.",
        )

    return update_rating(
        db=db,
        rating=rating,
        rating_data=rating_data,
    )


# =====================================================
# Delete Rating
# =====================================================

@router.delete(
    "/{rating_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rating_route(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rating = db.get(Rating, rating_id)

    if not rating:
        raise HTTPException(
            status_code=404,
            detail="Rating not found.",
        )

    if rating.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this rating.",
        )

    delete_rating(
        db=db,
        rating=rating,
    )