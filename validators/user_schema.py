from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import UploadFile, File


class CreateUser(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    username: str
    password: str
    photo: str


class GetUser(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    active: bool


class UserPhotos(BaseModel):
    photos: List[str]
