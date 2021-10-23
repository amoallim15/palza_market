from pydantic import Field, EmailStr, validator, constr, root_validator
from src.core.model import CoreModel, DateTimeModelMixin, IDModelMixin
from src.core.enums import UserRole, UserType, UserMethod
from typing import Optional


class UserBaseModel(CoreModel):
    email: EmailStr = Field(...)
    phone_no: str = Field(...)
    user_role: UserRole = UserRole.CLIENT
    #
    is_activated: bool = False
    is_email_verified: bool = False
    is_phone_no_verified: bool = False


class AgencyUserModelMixin(CoreModel):
    manager_phone_no: Optional[str]
    #
    business_name: str
    business_representative: str
    brokerage_record_no: str
    legal_address: str
    #
    business_registeration_no: str
    business_license_url: str
    brokerage_card_url: str

    @root_validator()
    def validate(cls, values):
        if values.get("user_type") == UserType.INDIVIDUAL:
            return values
        if (
            not values.get("business_name")
            or not values.get("business_representative")
            or not values.get("brokerage_record_no")
            or not values.get("legal_address")
            or not values.get("business_registeration_no")
            or not values.get("business_license_url")
            or not values.get("brokerage_card_url")
        ):
            raise ValueError("Agency information must be fully provided.")
        return values


class CreateUserModel(
    UserBaseModel, IDModelMixin, DateTimeModelMixin, AgencyUserModelMixin
):
    user_type: UserType = Field(...)
    user_method: UserMethod = Field(...)
    name: str = Field(...)
    username: constr(min_length=3, regex=r"^[a-zA-Z0-9_-]+$") = Field(...)
    personal_info_use_consent: bool = Field(...)
    terms_and_conditions_consent: bool = Field(...)
    #
    password: Optional[constr(min_length=6, max_length=100)]
    confirm_password: Optional[constr(min_length=6, max_length=100)]

    @validator("password", always=True)
    def validate_email_sign_up(cls, value, values):
        if values.get("user_method") == UserMethod.EMAIL and not values.get("password"):
            raise ValueError("Email sign up requires password.")
        return value

    @validator("confirm_password", always=True)
    def validate_confirm_password(cls, value, values):
        if "password" in values and values["confirm_password"] != values["password"]:
            raise ValueError("Passwords does not match.")
        return value

    @validator("personal_info_use_consent")
    def validate_personal_info_use_consent(cls, value, values):
        if value is False:
            raise ValueError("Personal info use consent is required.")
        return value

    @validator("terms_and_conditions_consent")
    def validate_terms_and_conditions_consent(cls, value, values):
        if value is False:
            raise ValueError("Terms and conditions consent is required.")
        return value


class UpdateUserModel(UserBaseModel, DateTimeModelMixin, AgencyUserModelMixin):
    display_name: str = Field(...)


class AuthenticateUserModel(CoreModel):
    username: str = Field(...)
    password: str = Field(...)


class ChangePasswordUserModel(CoreModel):
    password: str = Field(...)
    new_password: str = Field(...)
    confirm_new_password: str = Field(...)

    @validator("confirm_new_password", always=True)
    def validate_confirm_new_password(cls, value, values):
        if values["confirm_new_password"] != values["new_password"]:
            raise ValueError("New passwords does not match.")
        return value


class PatchUserModel(DateTimeModelMixin):
    user_type: Optional[UserType]
    name: Optional[str]
    #
    user_role: Optional[UserRole]
    is_activated: Optional[bool]
    is_email_verified: Optional[bool]
    is_phone_no_verified: Optional[bool]


class UserModel(UserBaseModel, IDModelMixin, DateTimeModelMixin, AgencyUserModelMixin):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    name: str = Field(...)
    username: str = Field(...)
    #
    display_name: Optional[str]

    @validator("display_name", always=True)
    def validate_display_name(cls, value, values):
        if value is None:
            return values["username"]
        return value
