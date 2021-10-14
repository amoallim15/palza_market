from pydantic import Field, HttpUrl
from src.core.model import CreateModel, UpdateModel
from typing import List
from src.core.enums import BannerLocation


class CreateBannerModel(CreateModel):
    width: int = Field(...)
    height: int = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    location: BannerLocation = Field(...)


class UpdateBannerModel(UpdateModel):
    width: int = Field(...)
    height: int = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    location: BannerLocation = Field(...)
