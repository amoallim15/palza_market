from pydantic import Field, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin


class SMSBaseModel(BaseModel):
    reciever_phone_no: str = Field(...)
    content: str = Field(...)


class SMSCountModel(BaseModel):
    count: int = Field(...)


class SMSSendModel(IDModelMixin, DateTimeModelMixin, SMSBaseModel):
    pass


class SMSModel(IDModelMixin, DateTimeModelMixin, SMSBaseModel):
    pass
