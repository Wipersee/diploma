import time
from models.oauth import OAuth2Client
from werkzeug.security import gen_salt
from dal import dal_client
from dal import dal_user
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

def delete_client(client_id: str, user_id: str):
    db_user = dal_user.get_by_id(id=user_id)
    db_client = dal_client.get_by_id(client_id=client_id)
    if db_user.id != db_client.user_id:
        return False
    if not dal_client.delete_oauth_code(client_id=db_client.client_id):
        return False
    if not dal_client.delete_oauth_token(client_id=db_client.client_id):
        return False
    if not dal_client.delete_oauth_client(client_id=db_client.client_id):
        return False
    return True