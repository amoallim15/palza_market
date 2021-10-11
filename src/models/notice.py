from pydantic import Field
from src.core.model import CreateModel, UpdateModel


class CreateNoticeModel(CreateModel):
    title: str = Field(...)
    thumbnail_url: str = Field(...)
    content: str = Field(...)


class UpdateNoticeModel(UpdateModel):
    title: str = Field(...)
    thumbnail_url: str = Field(...)
    content: str = Field(...)
