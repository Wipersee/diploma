from datetime import datetime
from pydantic import BaseModel, AnyUrl
from typing import List
from enum import Enum

class TokenEndpointAuthMethod(str, Enum):
    client_secret_basic="client_secret_basic"
    none="none"
    
class GetApp(BaseModel):
    id: int
    name: str
    login_url: str
    created_at: datetime


class CreateClient(BaseModel):
    name: str
    login_uri: AnyUrl
    allowed_scope: str
    redirect_uris: List[AnyUrl]
    allowed_grant_types: List[str]
    allowed_response_types: List[str]
    token_endpoint_auth_method: TokenEndpointAuthMethod
