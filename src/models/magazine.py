from pydantic import Field, HttpUrl, validator
from src.core.model import Model, UpdateModel


class MagazineModel(Model):
    image_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    new_source: str = Field(...)
    #
    views_count: int = Field(...)

    @validator("views_count", always=True)
    def validate_views_count(cls, value, values):
        if value is None:
            return 0
        return value


class UpdateMagazineModel(UpdateModel):
    image_url: HttpUrl = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    new_source: str = Field(...)


class IncrementViewsMagazineModel(Model):
    pass
