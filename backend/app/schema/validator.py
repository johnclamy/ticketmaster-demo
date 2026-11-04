from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import datetime
from app.models.review import Review
from app.schema.review import ReviewBase, ReviewUpdate


class ReviewValidator:
    """Validator class for review business logic."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def validate_rating(self, rating: int) -> None:
        """Validate rating is between 1 and 5."""
        if not 1 <= rating <= 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Rating must be between 1 and 5"
            )
    
    def validate_comment_length(self, comment: str) -> None:
        """Validate comment length."""
        if len(comment) < 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Comment must be at least 10 characters long"
            )
        if len(comment) > 1000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Comment must not exceed 1000 characters"
            )
    
    # def validate_user_exists(self, user_id: int) -> None:
    #     """Validate that the user exists."""
    #     from app.models.user import User
    #     user = self.session.get(User, user_id)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"User with id {user_id} not found"
    #         )
    
    # def validate_event_exists(self, event_id: int) -> None:
    #     """Validate that the event exists."""
    #     from app.models.event import Event
    #     event = self.session.get(Event, event_id)
    #     if not event:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Event with id {event_id} not found"
    #         )
    
    # def validate_user_purchased_ticket(self, user_id: int, event_id: int) -> None:
    #     """Validate that the user has purchased a ticket for the event."""
    #     from app.models.ticket import Ticket
    #     statement = select(Ticket).where(
    #         Ticket.user_id == user_id,
    #         Ticket.event_id == event_id
    #     )
    #     ticket = self.session.exec(statement).first()
    #     if not ticket:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="You can only review events you have purchased tickets for"
    #         )
    
    def validate_no_duplicate_review(self, user_id: int, event_id: int) -> None:
        """Validate that the user hasn't already reviewed this event."""
        statement = select(Review).where(
            Review.user_id == user_id,
            Review.event_id == event_id
        )
        existing_review = self.session.exec(statement).first()
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already reviewed this event"
            )
    
    def validate_review_exists(self, review_id: int) -> Review:
        """Validate that the review exists and return it."""
        review = self.session.get(Review, review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )
        return review
    
    def validate_review_ownership(self, review: Review, user_id: int) -> None:
        """Validate that the user owns the review."""
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own reviews"
            )
    
    # def validate_create(self, review_data: ReviewCreate) -> None:
    #     """Run all validations for creating a review."""
    #     self.validate_rating(review_data.rating)
    #     self.validate_comment_length(review_data.comment)
    #     self.validate_user_exists(review_data.user_id)
    #     self.validate_event_exists(review_data.event_id)
    #     self.validate_user_purchased_ticket(review_data.user_id, review_data.event_id)
    #     self.validate_no_duplicate_review(review_data.user_id, review_data.event_id)
    
    def validate_update(self, review: Review, update_data: ReviewUpdate, user_id: int) -> None:
        """Run all validations for updating a review."""
        self.validate_review_ownership(review, user_id)
        
        if update_data.rating is not None:
            self.validate_rating(update_data.rating)
        if update_data.comment is not None:
            self.validate_comment_length(update_data.comment)
