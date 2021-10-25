from pydantic import Field, HttpUrl, BaseModel
from src.core.model import IDModelMixin, DateTimeModelMixin, PyObjectId
from typing import List, Optional
from datetime import datetime


class RealstateBaseModel(BaseModel):
    display_name: Optional[str]
    lng: int = Field(...)
    lat: int = Field(...)
    user_id: PyObjectId = Field(...)
    image_urls: List[HttpUrl] = Field(...)
    count_down: datetime = Field(...)
    #
    legal_address: str = Field(...)
    m_name: str = Field(...)
    s_name: str = Field(...)
    quaranty: int = Field(..., ge=0)
    monthly_fee: int = Field(..., ge=0)
    premium: int = Field(..., ge=0)
    #
    mng_fee: Optional[str]
    #
    j_ofrs_stairs: int = Field(..., ge=0)
    total_stairs: int = Field(..., ge=0)
    r_floor_spaces: int = Field(..., ge=0)
    supply_space: float = Field(..., ge=0)
    #
    use_confirm_date: datetime = Field(...)
    #
    parking_total: int = Field(..., ge=0)
    director: str = Field(...)
    cont_name: str = Field(...)
    phone_no: str = Field(...)
    moving_day: str = Field(...)
    business_no: str = Field(...)
    registered_date: datetime = Field(...)
    title: str = Field(...)
    offer_explain: str = Field(...)
    sale_content: str = Field(...)
    interior_content: str = Field(...)
    volume_content: str = Field(...)
    etc_content: str = Field(...)


class CreateRealstateModel(IDModelMixin, DateTimeModelMixin, RealstateBaseModel):
    pass


class UpdateRealstateModel(DateTimeModelMixin, RealstateBaseModel):
    pass


class RealstateModel(IDModelMixin, DateTimeModelMixin, RealstateBaseModel):
    pass
