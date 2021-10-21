from pydantic import Field, HttpUrl
from src.core.model import Model, UpdateModel


class FranchiseModel(Model):
    thumbnail_url: HttpUrl = Field(...)
    external_url: HttpUrl = Field(...)
    store_count: int = Field(...)
    monthly_sales: int = Field(...)
    starting_cost: int = Field(...)


class UpdateFranchiseModel(UpdateModel):
    thumbnail_url: HttpUrl = Field(...)
    external_url: HttpUrl = Field(...)
    store_count: int = Field(...)
    monthly_sales: int = Field(...)
    starting_cost: int = Field(...)
