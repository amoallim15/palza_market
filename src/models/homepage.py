from pydantic import Field
from src.core.model import CreateModel, UpdateModel


class CreateHomePageSectionModel(CreateModel):
    section_type: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    background_image_url: str = Field(...)
    background_color: str = Field(...)
    height: int = Field(...)


class UpdateHomePageSectionModel(UpdateModel):
    section_type: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    background_image_url: str = Field(...)
    background_color: str = Field(...)
    height: int = Field(...)
