from pydantic import Field
from src.core.model import CreateModel, UpdateModel


class CreateReviewModel(CreateModel):
    realstate_id: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=10)


class UpdateReviewModel(UpdateModel):
    realstate_id: str = Field(...)
    content: str = Field(...)
    rating: int = Field(..., le=10)
