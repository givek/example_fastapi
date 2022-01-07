from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy.util.langhelpers import string_or_unprintable


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#
#
# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    author: UserResponse
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str


class Vote(BaseModel):
    post_id: int
    dir: int
