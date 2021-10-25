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


class DateTimeModelMixin(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None

    @validator("created_at", pre=True, always=True)
    def default_created_at(cls, value, values):
        return value or datetime.now()

    @validator("updated_at", pre=True, always=True)
    def default_updated_at(cls, value, values):
        return value or values["created_at"]


class IDModelMixin(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class ListModel(BaseModel):
    info: dict = Field(...)
    data: List[dict] = Field(default_factory=list)


class SuccessModel(BaseModel):
    status: int = 200
    detail: Optional[str]


class CoreModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        validate_assignment = True
        use_enum_values = True
