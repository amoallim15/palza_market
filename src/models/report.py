from pydantic import Field
from src.core.model import Model, UpdateModel


class ReportModel(Model):
    realstate_id: str = Field(...)
    content: str = Field(...)


class UpdateReportModel(UpdateModel):
    content: str = Field(...)
