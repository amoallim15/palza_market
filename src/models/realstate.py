from pydantic import Field, HttpUrl
from src.core.model import Model, UpdateModel
from typing import List, Optional


class RealstateModel(Model):
    display_name: str = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    lng: int = Field(...)
    lat: int = Field(...)


class UpdateRealstateModel(UpdateModel):
    display_name: str = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    lng: int = Field(...)
    lat: int = Field(...)


class PatchRealstateModel(Model):
    is_approved: Optional[bool]
