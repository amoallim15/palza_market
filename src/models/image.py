from pydantic import Field
from src.core.model import CreateModel


class CreateImageModel(CreateModel):
    file: str = Field(...)
