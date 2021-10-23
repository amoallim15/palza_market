from pydantic import Field
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin


class SMSBaseModel(CoreModel):
    reciever_phone_no: str = Field(...)
    content: str = Field(...)


class SMSSendModel(SMSBaseModel, IDModelMixin, DateTimeModelMixin):
    pass


class SMSCountModel(CoreModel):
    count: int = Field(...)


class SMSModel(SMSBaseModel, IDModelMixin, DateTimeModelMixin):
    pass
