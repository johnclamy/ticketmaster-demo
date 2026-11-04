from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlmodel import SQLModel


class ReviewBase(SQLModel):
    """Base schema with shared fields."""
    rating: int = Field(ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(
        min_length=10,
        max_length=1000,
        description="Review comment (10-1000 characters)"
    )


class ReviewCreate(ReviewBase):
    """Schema for creating a new review."""
    user_id: int = Field(description="ID of the user creating the review")
    event_id: int = Field(description="ID of the event being reviewed")


class ReviewUpdate(SQLModel):
    """Schema for updating an existing review. All fields optional."""
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = Field(default=None, min_length=10, max_length=1000)
    is_visible: Optional[bool] = None


class ReviewRead(ReviewBase):
    """Schema for reading/review responses."""
    id: int
    user_id: int
    event_id: int
    is_verified: bool
    is_visible: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True) # type: ignore


class ReviewReadWithUser(ReviewRead):
    """Review with user information included."""
    user_name: str = Field(description="Display name of the reviewer")
    user_avatar_url: Optional[str] = None


class ReviewListResponse(BaseModel):
    """Paginated list of reviews."""
    reviews: list[ReviewRead]
    total: int
    page: int
    per_page: int
    has_more: bool
