from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.booking import Booking
from app.models.rating import Rating
from app.models.ride import Ride
from app.models.user import User
from app.schemas.misc import RatingCreate, RatingUpdate


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def update_user_average_rating(db: Session, user_id: int) -> None:
    avg = db.scalar(
        select(func.avg(Rating.rating)).where(
            Rating.reviewee_id == user_id
        )
    )

    user = db.get(User, user_id)

    if user:
        user.average_rating = round(float(avg), 2) if avg else 0.0
        db.commit()


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_rating(
    db: Session,
    rating_data: RatingCreate,
    reviewer: User,
) -> Rating:

    ride = db.get(Ride, rating_data.ride_id)

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found.",
        )

    if reviewer.id == rating_data.reviewee_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot rate yourself.",
        )

    booking = db.scalar(
        select(Booking).where(
            Booking.ride_id == rating_data.ride_id,
            Booking.passenger_id == reviewer.id,
        )
    )

    if not booking and ride.driver_id != reviewer.id:
        raise HTTPException(
            status_code=400,
            detail="You were not part of this ride.",
        )

    existing = db.scalar(
        select(Rating).where(
            Rating.ride_id == rating_data.ride_id,
            Rating.reviewer_id == reviewer.id,
            Rating.reviewee_id == rating_data.reviewee_id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted a rating.",
        )

    rating = Rating(
        ride_id=rating_data.ride_id,
        reviewer_id=reviewer.id,
        reviewee_id=rating_data.reviewee_id,
        rating=rating_data.rating,
        review=rating_data.review,
    )

    db.add(rating)
    db.commit()
    db.refresh(rating)

    update_user_average_rating(db, rating.reviewee_id)

    return rating


# ---------------------------------------------------------
# Get Ratings
# ---------------------------------------------------------

def get_user_ratings(
    db: Session,
    user_id: int,
):
    return db.scalars(
        select(Rating)
        .where(Rating.reviewee_id == user_id)
        .order_by(Rating.created_at.desc())
    ).all()


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_rating(
    db: Session,
    rating: Rating,
    rating_data: RatingUpdate,
):

    data = rating_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(rating, key, value)

    db.commit()
    db.refresh(rating)

    update_user_average_rating(db, rating.reviewee_id)

    return rating


# ---------------------------------------------------------
# Delete
# ---------------------------------------------------------

def delete_rating(
    db: Session,
    rating: Rating,
):

    reviewee = rating.reviewee_id

    db.delete(rating)
    db.commit()

    update_user_average_rating(db, reviewee)