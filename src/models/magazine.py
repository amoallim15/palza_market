from pydantic import Field, HttpUrl
from src.core.model import CreateModel, UpdateModel
from typing import List
from src.core.enums import BannerLocation


class CreateMagazineModel(CreateModel):
    image_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    views_count: int = Field(...)
    new_source: str = Field(...)


class UpdateMagazineModel(UpdateModel):
    image_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    views_count: int = Field(...)
    new_source: str = Field(...)
