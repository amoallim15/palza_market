from pydantic import Field, HttpUrl
from src.core.model import Model, UpdateModel


class NoticeModel(Model):
    title: str = Field(...)
    thumbnail_url: HttpUrl = Field(...)
    content: str = Field(...)
    category_id: str = Field(...)


class UpdateNoticeModel(UpdateModel):
    title: str = Field(...)
    thumbnail_url: HttpUrl = Field(...)
    content: str = Field(...)
    category_id: str = Field(...)


class NoticeCategoryModel(Model):
    label: str = Field(...)


class UpdateNoticeCategoryModel(UpdateModel):
    label: str = Field(...)
