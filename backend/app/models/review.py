from sqlmodel import SQLModel, Field
from datetime import datetime


class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")
    rating: int = Field(ge=1, le=5)  # Rating should be between 1 and 5
    comment: str
    created_at: datetime = Field(default_factory=datetime.now)
