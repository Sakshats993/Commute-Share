from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.booking import Booking
from app.models.rating import Rating
from app.models.ride import Ride
from app.models.user import User
from app.models.enums import RideStatus
from app.schemas.misc import RatingCreate, RatingUpdate


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def update_user_average_rating(db: Session, user_id: int) -> None:
    """
    Updates a user's average rating and review count.
    """

    avg = db.scalar(
        select(func.avg(Rating.rating)).where(
            Rating.reviewee_id == user_id
        )
    )

    review_count = db.scalar(
        select(func.count(Rating.id)).where(
            Rating.reviewee_id == user_id
        )
    )

    user = db.get(User, user_id)

    if user:
        user.average_rating = (
            round(float(avg), 2)
            if avg is not None
            else 0.0
        )

        user.review_count = review_count or 0

        db.commit()

# ---------------------------------------------------------
# Create
# ---------------------------------------------------------
def get_rating_candidates(
    db: Session,
    current_user: User,
):
    """
    Return completed rides/bookings where the current user
    can still submit a rating.

    Passenger:
        Rates the driver.

    Driver:
        Rates each passenger who was booked on the ride.
    """

    results = []

    # ==================================================
    # Passenger
    # ==================================================

    if current_user.role == "passenger":

        bookings = db.scalars(
            select(Booking)
            .join(Booking.ride)
            .where(
                Booking.passenger_id == current_user.id,
                Ride.status == RideStatus.COMPLETED,
            )
            .order_by(
                Ride.departure_time.desc()
            )
        ).all()

        for booking in bookings:

            ride = booking.ride
            driver = ride.driver

            existing = db.scalar(
                select(Rating).where(
                    Rating.ride_id == ride.id,
                    Rating.reviewer_id == current_user.id,
                    Rating.reviewee_id == driver.id,
                )
            )

            if existing:
                continue

            results.append({
                "booking_id": booking.id,
                "ride_id": ride.id,
                "reviewee_id": driver.id,
                "reviewee_name": driver.full_name,
                "reviewee_role": "driver",
                "pickup_location": ride.pickup_location,
                "destination_location": ride.destination_location,
                "departure_time": ride.departure_time,
            })

    # ==================================================
    # Driver
    # ==================================================

    elif current_user.role == "driver":

        bookings = db.scalars(
            select(Booking)
            .join(Booking.ride)
            .where(
                Ride.driver_id == current_user.id,
                Ride.status == RideStatus.COMPLETED,
            )
            .order_by(
                Ride.departure_time.desc()
            )
        ).all()

        for booking in bookings:

            ride = booking.ride
            passenger = booking.passenger

            existing = db.scalar(
                select(Rating).where(
                    Rating.ride_id == ride.id,
                    Rating.reviewer_id == current_user.id,
                    Rating.reviewee_id == passenger.id,
                )
            )

            if existing:
                continue

            results.append({
                "booking_id": booking.id,
                "ride_id": ride.id,
                "reviewee_id": passenger.id,
                "reviewee_name": passenger.full_name,
                "reviewee_role": "passenger",
                "pickup_location": ride.pickup_location,
                "destination_location": ride.destination_location,
                "departure_time": ride.departure_time,
            })

    return results

def create_rating(
    db: Session,
    rating_data: RatingCreate,
    reviewer: User,
) -> Rating:

    booking = db.scalar(
        select(Booking).where(
            Booking.id == rating_data.booking_id,
        )
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    ride = db.get(Ride, booking.ride_id)

    if ride is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found.",
        )

    # --------------------------------------------------
    # Make sure the user participated in the ride
    # --------------------------------------------------

    is_passenger = (
        booking.passenger_id == reviewer.id
    )

    is_driver = (
        ride.driver_id == reviewer.id
    )

    if not is_passenger and not is_driver:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You were not part of this ride.",
        )

    # --------------------------------------------------
    # Determine who is being rated
    # --------------------------------------------------

    if is_passenger:
        # Passenger rates the driver
        reviewee_id = ride.driver_id

    else:
        # Driver rates this passenger
        reviewee_id = booking.passenger_id

    # --------------------------------------------------
    # Prevent self-rating
    # --------------------------------------------------

    if reviewer.id == reviewee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot rate yourself.",
        )

    # --------------------------------------------------
    # Only allow ratings after ride completion
    # --------------------------------------------------

    if ride.status != RideStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only rate users after the ride is completed.",
        )

    # --------------------------------------------------
    # Prevent duplicate rating
    # --------------------------------------------------

    existing = db.scalar(
        select(Rating).where(
            Rating.ride_id == ride.id,
            Rating.reviewer_id == reviewer.id,
            Rating.reviewee_id == reviewee_id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted a rating.",
        )

    # --------------------------------------------------
    # Create rating
    # --------------------------------------------------

    rating = Rating(
        ride_id=ride.id,
        reviewer_id=reviewer.id,
        reviewee_id=reviewee_id,
        rating=rating_data.rating,
        review=rating_data.review,
    )

    db.add(rating)
    db.commit()
    db.refresh(rating)

    update_user_average_rating(
        db,
        reviewee_id,
    )

    return rating_to_response_data(rating)

def rating_to_response_data(
    rating: Rating,
):
    return {
        "id": rating.id,
        "ride_id": rating.ride_id,
        "reviewer_id": rating.reviewer_id,
        "reviewer_name": rating.reviewer.full_name,
        "reviewer_role": (
            rating.reviewer.role.value
            if hasattr(rating.reviewer.role, "value")
            else str(rating.reviewer.role)
        ),
        "reviewee_id": rating.reviewee_id,
        "rating": rating.rating,
        "review": rating.review,
        "created_at": rating.created_at,
    }

# ---------------------------------------------------------
# Get Ratings
# ---------------------------------------------------------
def get_user_ratings(
    db: Session,
    user_id: int,
):
    ratings = db.scalars(
        select(Rating)
        .where(
            Rating.reviewee_id == user_id
        )
        .order_by(
            Rating.created_at.desc()
        )
    ).all()

    return [
        {
            "id": rating.id,
            "ride_id": rating.ride_id,
            "reviewer_id": rating.reviewer_id,
            "reviewer_name": rating.reviewer.full_name,
            "reviewer_role": (
                rating.reviewer.role.value
                if hasattr(rating.reviewer.role, "value")
                else str(rating.reviewer.role)
            ),
            "reviewee_id": rating.reviewee_id,
            "rating": rating.rating,
            "review": rating.review,
            "created_at": rating.created_at,
        }
        for rating in ratings
    ]
# ---------------------------------------------------------
# Get My Ratings
# ---------------------------------------------------------

def get_my_ratings(
    db: Session,
    current_user: User,
):
    """
    Return ratings received by the current user.
    """

    return get_user_ratings(
        db=db,
        user_id=current_user.id,
    )
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

    return rating_to_response_data(rating)


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