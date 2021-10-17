from pydantic import Field, EmailStr
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


class CreateUserModel(CreateModel):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    email: EmailStr = Field(...)
    name: str = Field(...)
    phone_no: str = Field(...)
    username: str = Field(...)
    # connection_info: str = Field(...)
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
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    display_name: str = Field(...)
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


class AuthenticateUserModel(UpdateModel):
    username: str = Field(...)
    password: str = Field(...)


class PatchUserModel(UpdateModel):
    user_role: Optional[UserRole]
    is_approved: Optional[bool]
