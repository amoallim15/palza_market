from pydantic import Field, validator
from src.core.model import Model
from typing import Optional, List


class WishlistModel(Model):
    user_id: str = Field(...)
    realstate_ids: Optional[List[str]]
    agency_ids: Optional[List[str]]

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


class PatchWishListModel(Model):
    user_id: str = Field(...)
    realstate_ids: Optional[List[str]]
    agency_ids: Optional[List[str]]
    operation: bool = Field(...)
