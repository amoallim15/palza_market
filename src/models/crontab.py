from pydantic import Field, validator
from src.core.model import Model, UpdateModel
from src.core.enums import CrontabStatus
from typing import Optional


class CrontabModel(Model):
    status: Optional[CrontabStatus]
    progress: Optional[int]

    @validator("status", always=True)
    def validate_status(cls, value, values):
        if value is None:
            return CrontabStatus.RUNNING
        return value

    @validator("progress", always=True)
    def validate_progress(cls, value, values):
        if value is None:
            return 0
        return value


class UpdateCrontabModel(UpdateModel):
    status: Optional[CrontabStatus]
    progress: int = Field(..., ge=0, le=100)
