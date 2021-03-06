import time
from models.oauth import OAuth2Client
from werkzeug.security import gen_salt
from utils.session import split_by_crlf
from dal import dal_client
from validators import client_schema


def create_client(data: client_schema.CreateClient, user_id: str):
    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user_id,
    )
    client_metadata = {
        "client_name": data.client_name,
        "client_uri": data.client_uri,
        "grant_types": data.grant_type,
        "redirect_uris": data.redirect_uri,
        "response_types": data.response_type,
        "scope": data.scope,
        "token_endpoint_auth_method": data.token_endpoint_auth_method,
    }
    client.set_client_metadata(client_metadata)
    if data.token_endpoint_auth_method == "none":
        client.client_secret = ""
    else:
        client.client_secret = gen_salt(48)
    return dal_client.create(client=client), client_metadata
