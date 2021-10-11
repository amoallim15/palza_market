from pydantic import BaseModel, Field
from src.core.model import CreateModel, UpdateModel
from typing import List, Optional


class CreateRealstateModel(CreateModel):
    display_name: str = Field(...)
    image_urls: List[str] = Field(...)
    lng: int = Field(...)
    lat: int = Field(...)


class UpdateRealstateModel(UpdateModel):
    display_name: str = Field(...)
    image_urls: List[str] = Field(...)
    lng: int = Field(...)
    lat: int = Field(...)


class PatchRealstateModel(BaseModel):
    is_approved: Optional[bool]
    is_liked: Optional[bool]