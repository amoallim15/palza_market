from pydantic import Field, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin, PyObjectId
from src.core.enums import ReviewType


class ReviewBaseModel(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=5)


class CreateReviewModel(IDModelMixin, DateTimeModelMixin, ReviewBaseModel):
    agency_id: PyObjectId = Field(...)
    review_type: ReviewType = Field(...)


class UpdateReviewModel(DateTimeModelMixin, ReviewBaseModel):
    pass


class ReviewModel(IDModelMixin, DateTimeModelMixin, ReviewBaseModel):
    user_id: PyObjectId = Field(...)
    agency_id: PyObjectId = Field(...)
    review_type: ReviewType = Field(...)
    user: dict = Field(...)
    agency: dict = Field(...)
