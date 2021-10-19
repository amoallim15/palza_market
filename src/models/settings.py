from pydantic import Field
from src.core.model import Model


class SettingsModel(Model):
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
