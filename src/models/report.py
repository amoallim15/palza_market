from pydantic import Field
from src.core.model import CreateModel, UpdateModel


class CreateReportModel(CreateModel):
    realstate_id: str = Field(...)
    content: str = Field(...)


class UpdateReportModel(UpdateModel):
    content: str = Field(...)
