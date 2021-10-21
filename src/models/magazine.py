from pydantic import Field, HttpUrl, validator
from src.core.model import Model, UpdateModel


class MagazineModel(Model):
    thumbnail_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    news_source: str = Field(...)
    #
    view_count: int = Field(...)

    @validator("view_count", always=True)
    def validate_view_count(cls, value, values):
        if value is None:
            return 0
        return value


class UpdateMagazineModel(UpdateModel):
    thumbnail_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    news_source: str = Field(...)


class IncrementViewsMagazineModel(UpdateModel):
    pass
