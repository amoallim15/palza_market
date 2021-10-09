from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    user_id: UUID
    method: str
    username: str
    password: str
    email: str
    connInfo: str
    display_name: str
    role: str


class Realstate(BaseModel):
    display_name: str


class Post(BaseModel):
    # user_id: UUID
    # post_id: UUID
    title: str
    content: str
    thumbnail: Optional[str] = None


class Comment(BaseModel):
    # user_id: UUID
    # post_id: UUID
    # comment_id: UUID
    content: str


class Notice(BaseModel):
    # user_id: UUID
    title: str
    content: str


class SMS(BaseModel):
    # user_id: UUID
    reciver_phone_no: str
    content: str
