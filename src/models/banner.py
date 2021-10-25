from pydantic import Field, HttpUrl, BaseModel
from src.core.model import DateTimeModelMixin
from typing import List
from src.core.enums import BannerLocation


class BannerBaseModel(BaseModel):
    width: int = Field(...)
    height: int = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    location: BannerLocation = Field(...)


class UpdateBannerModel(DateTimeModelMixin, BannerBaseModel):
    pass


class BannerModel(DateTimeModelMixin, BannerBaseModel):
    pass
