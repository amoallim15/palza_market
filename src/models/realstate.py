from pydantic import Field, HttpUrl
from src.core.model import CreateModel, UpdateModel
from typing import List, Optional


class CreateRealstateModel(CreateModel):
    display_name: str = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    lng: int = Field(...)
    lat: int = Field(...)


class UpdateRealstateModel(UpdateModel):
    display_name: str = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    lng: int = Field(...)
    lat: int = Field(...)


class PatchRealstateModel(UpdateModel):
    is_approved: Optional[bool]
