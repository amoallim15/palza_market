from pydantic import Field, validator
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin
from src.core.enums import CrontabStatus
from typing import Optional


class CrontabModel(CoreModel):
    status: CrontabStatus = Field(...)
    progress: int = Field(..., ge=0, le=100)

    @validator("progress", always=True)
    def validate_progress(cls, value, values):
        if value is None:
            return 0
        return value


class CreateCrontabModel(CrontabModel, IDModelMixin, DateTimeModelMixin):
    @validator("status", always=True)
    def validate_status(cls, value, values):
        if value is None:
            return CrontabStatus.CREATED
        return value


class UpdateCrontabModel(CrontabModel, DateTimeModelMixin):
    status: Optional[CrontabStatus]
    progress: int = Field(..., ge=0, le=100)
