from datetime import datetime
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


class PutUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr

class UserPassword(BaseModel):
    old_password: str
    password: str

class UserPhotos(BaseModel):
    photos: List[str]

class GetUnauth(BaseModel):
    date: datetime
    type: str
    similarity: str

class GetUnauths(BaseModel):
    logins: List[GetUnauth]

class GetLine(BaseModel):
    date: datetime
    value: int

class GetPie(BaseModel):
    type: str
    value: int

class GetDash(BaseModel):
    line: List[GetLine]
    pie: List[GetPie]