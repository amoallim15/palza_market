from pydantic import Field
from src.core.model import UpdateModel


class UpdateSettingsModel(UpdateModel):
    title: str = Field(...)
    dsecription: str = Field(...)
    #
    kakao_key: str = Field(...)
    naver_key: str = Field(...)
    nice_key: str = Field(...)
    gambia_key: str = Field(...)
    nsdi_key: str = Field(...)
