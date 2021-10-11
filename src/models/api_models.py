# from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from src.core.enums import UserRole, UserType, UserMethod
from typing import List


class User(BaseModel):
    user_id: UUID
    user_method: UserMethod
    user_type: UserType
    user_role: UserRole
    user_state: bool
    username: str
    password: str
    email: str
    display_name: str


class Realstate(BaseModel):
    display_name: str
    image_urls: List[str]
    is_approved: bool
    lng: int
    lat: int


class Notice(BaseModel):
    # user_id: UUID
    title: str
    thumbnail_url: str
    content: str


class Report(BaseModel):
    # user_id: UUID
    realstate_id: UUID
    content: str


class SMS(BaseModel):
    # user_id: UUID
    reciever_phone_no: str
    content: str


class HomePageSection(BaseModel):
    section_type: str
    title: str
    content: str
    background_image_url: str
    background_color: str
    height: int


class Review(BaseModel):
    realstate_id: UUID
    content: str
    rating: int
