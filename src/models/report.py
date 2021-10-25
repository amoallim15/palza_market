from pydantic import Field, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin, PyObjectId


class ReportBaseModel(BaseModel):
    content: str = Field(...)


class CreateReportModel(IDModelMixin, DateTimeModelMixin, ReportBaseModel):
    realstate_id: str = Field(...)


class UpdateReportModel(DateTimeModelMixin, ReportBaseModel):
    pass


class ReportModel(IDModelMixin, DateTimeModelMixin, ReportBaseModel):
    user_id: PyObjectId = Field(...)
    realstate_id: PyObjectId = Field(...)
    user: dict = Field(...)
    realstate: dict = Field(...)
