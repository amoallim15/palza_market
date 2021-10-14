from pydantic import Field, EmailStr
from src.core.model import CreateModel, UpdateModel
from src.core.enums import UserRole, UserType, UserMethod
from typing import Optional


class CreateUserModel(CreateModel):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    phone_no: str = Field(...)
    display_name: str = Field(...)


class UpdateUserModel(UpdateModel):
    user_method: UserMethod = Field(...)
    user_type: UserType = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    display_name: str = Field(...)


class AuthenticateUserModel(UpdateModel):
    username: str = Field(...)
    password: str = Field(...)
    method: Optional[UserMethod]


class PatchUserModel(UpdateModel):
    user_role: Optional[UserRole]
    is_approved: Optional[bool]
