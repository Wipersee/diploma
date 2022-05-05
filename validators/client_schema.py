from datetime import datetime
from pydantic import BaseModel, AnyUrl
from typing import List
from enum import Enum


class TokenEndpointAuthMethod(str, Enum):
    client_secret_basic = "client_secret_basic"
    none = "none"


class CreateClient(BaseModel):
    client_name: str
    client_uri: AnyUrl
    scope: str
    redirect_uri: List[AnyUrl]
    grant_type: List[str]
    response_type: List[str]
    token_endpoint_auth_method: TokenEndpointAuthMethod


class GetClient(BaseModel):
    id: str
    client_id: str
    client_secret: str
    client_metadata: CreateClient


class GetGrantAccess(BaseModel):
    scope: str
    client_name: str
    expires_in: datetime
    issued_at: datetime
    client_uri: str
    id: int
    token: str


class GetGrantAccessList(BaseModel):
    access: List[GetGrantAccess]


class GetClients(BaseModel):
    clients: List[GetClient]
