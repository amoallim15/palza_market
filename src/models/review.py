from pydantic import Field
from src.core.model import Model, UpdateModel
from src.core.enums import ReviewType


class ReviewModel(Model):
    user_id: str = Field(...)
    agency_id: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=10)
    review_type: ReviewType = Field(...)


class UpdateReviewModel(UpdateModel):
    title: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=10)
