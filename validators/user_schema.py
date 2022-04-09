from typing import List, Optional
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    active: bool
    password: str
