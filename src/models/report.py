from pydantic import Field
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin


class ReportBaseModel(CoreModel):
    content: str = Field(...)


class CreateReportModel(ReportBaseModel, IDModelMixin, DateTimeModelMixin):
    realstate_id: str = Field(...)


class UpdateReportModel(ReportBaseModel, DateTimeModelMixin):
    pass


class ReportModel(ReportBaseModel, IDModelMixin, DateTimeModelMixin):
    user_id: str = Field(...)
    realstate_id: str = Field(...)
    user: dict = Field(...)
    realstate: dict = Field(...)
