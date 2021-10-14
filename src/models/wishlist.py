from pydantic import Field
from src.core.model import UpdateModel
from typing import Optional, List


class PatchWishlistModel(UpdateModel):
    realstate_ids: Optional[List[str]]
    agency_ids: Optional[List[str]]
    operation: bool = Field(...)
