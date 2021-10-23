from pydantic import Field, HttpUrl, validator
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin
from typing import Optional


class MagazineBaseModel(CoreModel):
    thumbnail_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    news_source: str = Field(...)
    magazine_type: str = Field(...)


class CreateMagazineModel(MagazineBaseModel, IDModelMixin, DateTimeModelMixin):
    pass


class UpdateMagazineModel(MagazineBaseModel, DateTimeModelMixin):
    pass


class PatchMagazineModel(MagazineBaseModel, DateTimeModelMixin):
    pass


class MagazineModel(MagazineBaseModel, IDModelMixin, DateTimeModelMixin):
    view_count: Optional[int]

    @validator("view_count", always=True)
    def validate_view_count(cls, value, values):
        if value is None:
            return 0
        return value
