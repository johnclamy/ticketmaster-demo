from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import UniqueConstraint, Index


class Review(SQLModel, table=True):
    """
    Review model representing a user's review for an event.
    """
    __tablename__ = "reviews" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    event_id: int = Field(foreign_key="event.id")

    # Rating should be between 1 and 5
    rating: int = Field(ge=1, le=5)

    # Comment with length constraints
    comment: str = Field(min_length=10, max_length=1000, nullable=False)

    # Metadata fields
    is_verified: bool = Field(default=False, description="True if user purchased a ticket")
    is_visible: bool = Field(default=True, description="False if review is hidden by moderation")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    # Table constraints
    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_user_event_review"),
        Index("ix_reviews_rating", "rating"),
        Index("ix_reviews_created_at", "created_at"),
    )
