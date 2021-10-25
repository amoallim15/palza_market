from pydantic import Field, validator, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin, PyObjectId
from typing import List


class WishlistBaseModel(BaseModel):
    realstate_ids: List[PyObjectId] = Field(default_factory=list)
    agency_ids: List[PyObjectId] = Field(default_factory=list)

    @validator("realstate_ids", always=True)
    def validate_realstate_ids(cls, value, values):
        if value is None:
            return []
        return value

    @validator("agency_ids", always=True)
    def validate_agency_ids(cls, value, values):
        if value is None:
            return []
        return value


class PatchWishlistModel(DateTimeModelMixin, WishlistBaseModel):
    operation: bool = Field(...)


class WishlistModel(IDModelMixin, DateTimeModelMixin, WishlistBaseModel):
    user_id: PyObjectId = Field(...)
