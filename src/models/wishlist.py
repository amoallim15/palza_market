from pydantic import Field, validator
from src.core.model import Model
from typing import Optional, List


class WishlistModel(Model):
    user_id: str = Field(...)
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


class PatchWishlistModel(Model):
    realstate_ids: List[str] = Field(default_factory=list)
    agency_ids: List[str] = Field(default_factory=list)
    operation: bool = Field(...)
