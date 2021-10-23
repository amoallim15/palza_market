from pydantic import Field
from src.core.model import DateTimeModelMixin


class SettingsModel(DateTimeModelMixin):
    title: str = Field(...)
    description: str = Field(...)
    fax_no: str = Field(...)
    #
    kakao_key: str = Field(...)
    naver_key: str = Field(...)
    google_key: str = Field(...)
    gabia_sms_id: str = Field(...)
    gabia_sms_key: str = Field(...)
    gabia_sms_callback_number: str = Field(...)
    nsdi_key: str = Field(...)
    odcloud_key: str = Field(...)
