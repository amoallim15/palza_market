from pydantic import Field
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin
from src.core.enums import ReviewType


class ReviewBaseModel(CoreModel):
    title: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=5)


class CreateReviewModel(ReviewBaseModel, IDModelMixin, DateTimeModelMixin):
    agency_id: str = Field(...)
    review_type: ReviewType = Field(...)


class UpdateReviewModel(ReviewBaseModel, DateTimeModelMixin):
    pass


class ReviewModel(ReviewBaseModel, IDModelMixin, DateTimeModelMixin):
    user_id: str = Field(...)
    agency_id: str = Field(...)
    review_type: ReviewType = Field(...)
    user: dict = Field(...)
    agency: dict = Field(...)
