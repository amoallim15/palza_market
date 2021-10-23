from pydantic import Field, validator
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin
from typing import List


class WishlistBaseModel(CoreModel):
    realstate_ids: List[str] = Field(default_factory=list)
    agency_ids: List[str] = Field(default_factory=list)

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


class PatchWishlistModel(WishlistBaseModel, DateTimeModelMixin):
    operation: bool = Field(...)


class WishlistModel(WishlistBaseModel, IDModelMixin, DateTimeModelMixin):
    user_id: str = Field(...)
