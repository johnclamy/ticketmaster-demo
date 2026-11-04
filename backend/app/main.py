from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime

# from app.database import get_session
from app.models.review import Review
from app.schema.review import ReviewCreate, ReviewUpdate, ReviewRead
# from app.validators.review import ReviewValidator

router = APIRouter(prefix="/reviews", tags=["reviews"])


# @router.post("/", response_model=ReviewRead, status_code=201)
# def create_review(
#     review_data: ReviewCreate,
#     session: Session = Depends(get_session)
# )
#     """Create a new review."""
#     validator = ReviewValidator(session)
#     validator.validate_create(review_data)
    
#     review = Review(
#         **review_data.model_dump(),
#         is_verified=True  # Set to True since we validated ticket purchase
#     )
#     session.add(review)
#     session.commit()
#     session.refresh(review)
    
#     return review


# @router.patch("/{review_id}", response_model=ReviewRead)
# def update_review(
#     review_id: int,
#     update_data: ReviewUpdate,
#     user_id: int,  # This would come from auth dependency
#     session: Session = Depends(get_session)
# ):
#     """Update an existing review."""
#     validator = ReviewValidator(session)
#     review = validator.validate_review_exists(review_id)
#     validator.validate_update(review, update_data, user_id)
    
#     update_dict = update_data.model_dump(exclude_unset=True)
#     for key, value in update_dict.items():
#         setattr(review, key, value)
    
#     review.updated_at = datetime.utcnow()
    
#     session.add(review)
#     session.commit()
#     session.refresh(review)
    
#     return review


# @router.get("/{review_id}", response_model=ReviewRead)
# def get_review(
#     review_id: int,
#     session: Session = Depends(get_session)
# ):
#     """Get a review by ID."""
#     validator = ReviewValidator(session)
#     review = validator.validate_review_exists(review_id)
#     return review