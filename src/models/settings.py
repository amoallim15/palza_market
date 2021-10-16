from pydantic import Field
from src.core.model import CreateModel, UpdateModel
from typing import Optional


class CreateSettingsModel(CreateModel):
    title: str = Field(...)
    dsecription: Optional[str]
    fax_no: str = Field(...)
    #
    kakao_key: str = Field(...)
    naver_key: str = Field(...)
    nice_key: str = Field(...)
    gambia_key: str = Field(...)
    nsdi_key: str = Field(...)
    odcloud_key: str = Field(...)


class UpdateSettingsModel(UpdateModel):
    title: str = Field(...)
    dsecription: str = Field(...)
    fax_no: str = Field(...)
    #
    kakao_key: str = Field(...)
    naver_key: str = Field(...)
    nice_key: str = Field(...)
    gambia_key: str = Field(...)
    nsdi_key: str = Field(...)
    odcloud_key: str = Field(...)
