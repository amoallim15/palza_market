from pydantic import Field, EmailStr, validator
from src.core.model import Model, UpdateModel
from src.core.enums import UserRole, UserType, UserMethod
from typing import Optional


class UserModel(Model):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    # Not Optional
    user_role: Optional[UserRole]
    #
    email: EmailStr = Field(...)
    name: str = Field(...)
    phone_no: str = Field(...)
    username: str = Field(...)
    #
    is_approved: Optional[bool]
    #
    manager_phone_no: Optional[str]
    #
    business_name: Optional[str]
    business_representative: Optional[str]
    brokerage_record_no: Optional[str]
    legal_address: Optional[str]
    #
    business_registeration_no: Optional[str]
    business_license_url: Optional[str]
    brokerage_card_url: Optional[str]

    @validator("user_role", always=True)
    def validate_user_role(cls, value, values):
        if value is None:
            return UserRole.CLIENT
        return value

    @validator("is_approved", always=True)
    def validate_is_approved(cls, value, values):
        if value is None:
            return False
        return value


class CreateUserModel(Model):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    #
    email: EmailStr = Field(...)
    name: str = Field(...)
    phone_no: str = Field(...)
    username: str = Field(...)
    #
    password: Optional[str]
    #
    manager_phone_no: Optional[str]
    #
    business_name: Optional[str]
    business_representative: Optional[str]
    brokerage_record_no: Optional[str]
    legal_address: Optional[str]
    #
    business_registeration_no: Optional[str]
    business_license_url: Optional[str]
    brokerage_card_url: Optional[str]


class UpdateUserModel(UpdateModel):
    email: EmailStr = Field(...)
    phone_no: str = Field(...)
    display_name: str = Field(...)
    #
    manager_phone_no: Optional[str]
    #
    business_name: Optional[str]
    business_representative: Optional[str]
    brokerage_record_no: Optional[str]
    legal_address: Optional[str]
    #
    business_registeration_no: Optional[str]
    business_license_url: Optional[str]
    brokerage_card_url: Optional[str]


class AuthenticateUserModel(Model):
    username: str = Field(...)
    password: str = Field(...)


class ChangePasswordUserModel(Model):
    password: str = Field(...)
    new_password: str = Field(...)
    confirm_new_password: str = Field(...)


class PatchUserModel(Model):
    user_role: Optional[UserRole]
    user_type: Optional[UserType]
    #
    name: Optional[str]
    #
    is_approved: Optional[bool]
