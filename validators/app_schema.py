from datetime import datetime
from pydantic import BaseModel, AnyUrl


class GetApp(BaseModel):
    id: int
    name: str
    login_url: str
    created_at: datetime


class CreateApp(BaseModel):
    name: str
    login_url: AnyUrl
