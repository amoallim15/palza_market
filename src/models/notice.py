from pydantic import Field, HttpUrl, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin, PyObjectId


class NoticeBaseModel(BaseModel):
    title: str = Field(...)
    thumbnail_url: HttpUrl = Field(...)
    content: str = Field(...)
    category_id: PyObjectId = Field(...)


class CreateNoticeModel(IDModelMixin, DateTimeModelMixin, NoticeBaseModel):
    pass


class UpdateNoticeModel(DateTimeModelMixin, NoticeBaseModel):
    pass


class NoticeModel(IDModelMixin, DateTimeModelMixin, NoticeBaseModel):
    category: dict = Field(...)


class NoticeCategorBaseModel(BaseModel):
    label: str = Field(...)


class CreateNoticeCategoryModel(
    IDModelMixin, DateTimeModelMixin, NoticeCategorBaseModel
):
    pass


class UpdateNoticeCategoryModel(DateTimeModelMixin, NoticeCategorBaseModel):
    pass


class NoticeCategoryModel(IDModelMixin, DateTimeModelMixin, NoticeCategorBaseModel):
    pass
