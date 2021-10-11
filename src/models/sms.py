from pydantic import Field
from src.core.model import CreateModel


class CreateSMSModel(CreateModel):
    reciever_phone_no: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
