from pydantic import Field, HttpUrl, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin


class FranchiseBaseModel(BaseModel):
    thumbnail_url: HttpUrl = Field(...)
    external_url: HttpUrl = Field(...)
    store_count: int = Field(...)
    monthly_sales: int = Field(...)
    starting_cost: int = Field(...)


class CreateFranchiseModel(IDModelMixin, DateTimeModelMixin, FranchiseBaseModel):
    pass


class UpdateFranchiseModel(DateTimeModelMixin, FranchiseBaseModel):
    pass


class FranchiseModel(IDModelMixin, DateTimeModelMixin, FranchiseBaseModel):
    pass
