from pydantic import Field
from src.core.model import Model


class SMSModel(Model):
    reciever_phone_no: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)

class SMSCountModel(Model):
    count: int = Field(...)