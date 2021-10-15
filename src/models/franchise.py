from pydantic import Field, HttpUrl
from src.core.model import CreateModel, UpdateModel
from typing import List
from src.core.enums import BannerLocation


class CreateFranchiseModel(CreateModel):
    image_url: HttpUrl = Field(...)
    external_url: HttpUrl = Field(...)
    store_count: int = Field(...)
    monthly_sales: int = Field(...)
    starting_cost: int = Field(...)


class UpdateFranchiseModel(UpdateModel):
    image_url: HttpUrl = Field(...)
    external_url: HttpUrl = Field(...)
    store_count: int = Field(...)
    monthly_sales: int = Field(...)
    starting_cost: int = Field(...)