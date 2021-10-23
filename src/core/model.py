from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import List, Optional
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CoreModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        validate_assignment = True


class DateTimeModelMixin(CoreModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", always=True)
    def validate_created_at(cls, value: datetime):
        return value or datetime.now()

    @validator("updated_at", always=True)
    def validate_updated_at(cls, value: datetime):
        return datetime.now()


class IDModelMixin(CoreModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class ListModel(CoreModel):
    keywords: Optional[str]
    count: int = Field(...)
    page: int = Field(...)
    data: List[dict] = Field(...)


class SuccessModel(CoreModel):
    status: int = 200
    detail: Optional[str]
