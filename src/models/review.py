from pydantic import Field
from src.core.model import Model, UpdateModel


class ReviewModel(Model):
    user_id: str = Field(...)
    agency_id: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=10)


class UpdateReviewModel(UpdateModel):
    content: str = Field(...)
    rating: int = Field(..., le=10)
