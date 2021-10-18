from pydantic import Field, EmailStr, validator
from src.core.model import ResModel, CreateModel, UpdateModel
from src.core.enums import UserRole, UserType, UserMethod
from typing import Optional


class UserModel(ResModel):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    email: EmailStr = Field(...)
    name: str = Field(...)
    phone_no: str = Field(...)
    username: str = Field(...)
    display_name: Optional[str]
    #
    user_role: UserRole = UserRole.CLIENT
    is_approved: bool = False
    #
    business_name: Optional[str] = Field(...)
    business_representative: Optional[str]
    brokerage_record_no: Optional[str]
    legal_address: Optional[str]
    #
    manager_phone_no: Optional[str]
    business_registeration_no: Optional[str]
    business_license_url: Optional[str]
    brokerage_card_url: Optional[str]

    @validator("display_name", always=True)
    def validate_display_name(cls, value, values):
        if value is None:
            return values["username"]
        return value


class CreateUserModel(CreateModel):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    email: EmailStr = Field(...)
    name: str = Field(...)
    phone_no: str = Field(...)
    username: str = Field(...)
    #
    password: Optional[str]
    #
    business_name: Optional[str]
    business_representative: Optional[str]
    brokerage_record_no: Optional[str]
    legal_address: Optional[str]
    #
    manager_phone_no: Optional[str]
    business_registeration_no: Optional[str]
    business_license_url: Optional[str]
    brokerage_card_url: Optional[str]


class UpdateUserModel(UpdateModel):
    email: EmailStr = Field(...)
    phone_no: str = Field(...)
    username: str = Field(...)
    display_name: str = Field(...)
    #
    manager_phone_no: Optional[str]


class AuthenticateUserModel(UpdateModel):
    username: str = Field(...)
    password: str = Field(...)


class ChangePasswordModel(UpdateModel):
    password: str = Field(...)
    new_password: str = Field(...)


class PatchUserModel(UpdateModel):
    user_role: Optional[UserRole]
    is_approved: Optional[bool]
    user_type: Optional[UserType]
