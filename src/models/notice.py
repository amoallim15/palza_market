from pydantic import Field, HttpUrl
from src.core.model import CreateModel, UpdateModel


class CreateNoticeModel(CreateModel):
    title: str = Field(...)
    thumbnail_url: HttpUrl = Field(...)
    content: str = Field(...)


class UpdateNoticeModel(UpdateModel):
    title: str = Field(...)
    thumbnail_url: HttpUrl = Field(...)
    content: str = Field(...)
