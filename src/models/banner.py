from pydantic import Field, HttpUrl
from src.core.model import Model, UpdateModel
from typing import List
from src.core.enums import BannerLocation


class BannerModel(Model):
    width: int = Field(...)
    height: int = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    location: BannerLocation = Field(...)
