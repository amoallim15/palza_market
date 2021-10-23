from pydantic import Field, HttpUrl
from src.core.model import CoreModel, IDModelMixin, DateTimeModelMixin


class FranchiseBaseModel(CoreModel):
    thumbnail_url: HttpUrl = Field(...)
    external_url: HttpUrl = Field(...)
    store_count: int = Field(...)
    monthly_sales: int = Field(...)
    starting_cost: int = Field(...)


class CreateFranchiseModel(FranchiseBaseModel, IDModelMixin, DateTimeModelMixin):
    pass


class UpdateFranchiseModel(FranchiseBaseModel, DateTimeModelMixin):
    pass


class FranchiseModel(FranchiseBaseModel, IDModelMixin, DateTimeModelMixin):
    pass
