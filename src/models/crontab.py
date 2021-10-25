from pydantic import Field, validator, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin
from src.core.enums import CrontabStatus
from typing import Optional


class CrontabModel(BaseModel):
    status: CrontabStatus = Field(...)
    progress: int = Field(..., ge=0, le=100)

    @validator("progress", always=True)
    def validate_progress(cls, value, values):
        if value is None:
            return 0
        return value


class CreateCrontabModel(IDModelMixin, DateTimeModelMixin, CrontabModel):
    @validator("status", always=True)
    def validate_status(cls, value, values):
        if value is None:
            return CrontabStatus.CREATED
        return value


class UpdateCrontabModel(DateTimeModelMixin, CrontabModel):
    status: Optional[CrontabStatus]
    progress: int = Field(..., ge=0, le=100)
