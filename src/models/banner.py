from pydantic import Field, HttpUrl
from src.core.model import CoreModel, DateTimeModelMixin
from typing import List
from src.core.enums import BannerLocation


class BannerBaseModel(CoreModel):
    width: int = Field(...)
    height: int = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    location: BannerLocation = Field(...)


class UpdateBannerModel(BannerBaseModel, DateTimeModelMixin):
    pass


class BannerModel(BannerBaseModel, DateTimeModelMixin):
    pass
