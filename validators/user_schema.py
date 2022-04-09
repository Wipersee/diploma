from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import UploadFile, File

class CreateUser(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    active: bool
    password: str
    photos: List[UploadFile] = File(...)

class GetUser(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    active: bool