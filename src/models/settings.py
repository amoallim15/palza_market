from pydantic import Field
from src.core.model import CreateModel, UpdateModel, ResModel
from typing import Optional


class CreateSettingsModel(CreateModel):
    title: str = Field(...)
    description: Optional[str]
    fax_no: str = Field(...)
    #
    kakao_key: str = Field(...)
    naver_key: str = Field(...)
    google_key: str = Field(...)
    gabia_key: str = Field(...)
    nsdi_key: str = Field(...)
    odcloud_key: str = Field(...)


class UpdateSettingsModel(UpdateModel):
    title: str = Field(...)
    description: str = Field(...)
    fax_no: str = Field(...)
    #
    kakao_key: str = Field(...)
    naver_key: str = Field(...)
    google_key: str = Field(...)
    gabia_key: str = Field(...)
    nsdi_key: str = Field(...)
    odcloud_key: str = Field(...)


class SettingsModel(ResModel):
    title: Optional[str]
    description: Optional[str]
    fax_no: Optional[str]
    #
    kakao_key: Optional[str]
    naver_key: Optional[str]
    google_key: Optional[str]
    gabia_key: Optional[str]
    nsdi_key: Optional[str]
    odcloud_key: Optional[str]
