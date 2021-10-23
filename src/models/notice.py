from pydantic import Field, HttpUrl
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin


class NoticeBaseModel(CoreModel):
    title: str = Field(...)
    thumbnail_url: HttpUrl = Field(...)
    content: str = Field(...)
    category_id: str = Field(...)


class CreateNoticeModel(NoticeBaseModel, IDModelMixin, DateTimeModelMixin):
    pass


class UpdateNoticeModel(NoticeBaseModel, DateTimeModelMixin):
    pass


class NoticeModel(NoticeBaseModel, IDModelMixin, DateTimeModelMixin):
    category: dict = Field(...)


class NoticeCategorBaseModel(CoreModel):
    label: str = Field(...)


class CreateNoticeCategoryModel(
    NoticeCategorBaseModel, IDModelMixin, DateTimeModelMixin
):
    pass


class UpdateNoticeCategoryModel(NoticeCategorBaseModel, DateTimeModelMixin):
    pass


class NoticeCategoryModel(NoticeCategorBaseModel, IDModelMixin, DateTimeModelMixin):
    pass
