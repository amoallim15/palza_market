from pydantic import Field, HttpUrl, validator, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin
from typing import Optional


class MagazineBaseModel(BaseModel):
    thumbnail_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    news_source: str = Field(...)
    magazine_type: str = Field(...)


class CreateMagazineModel(IDModelMixin, DateTimeModelMixin, MagazineBaseModel):
    pass


class UpdateMagazineModel(DateTimeModelMixin, MagazineBaseModel):
    pass


class PatchMagazineModel(DateTimeModelMixin, MagazineBaseModel):
    pass


class MagazineModel(IDModelMixin, DateTimeModelMixin, MagazineBaseModel):
    view_count: Optional[int]

    @validator("view_count", always=True)
    def validate_view_count(cls, value, values):
        if value is None:
            return 0
        return value
