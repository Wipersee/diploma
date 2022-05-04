from flask import Blueprint, jsonify
from flask_pydantic import validate
from utils.session import login_required
from handlers.client import create_client, delete_client
from validators import client_schema
from dal import dal_client
from flask_cors import cross_origin

client_api_router = Blueprint("api_client", __name__)


@client_api_router.route("/", methods=("GET",))
@cross_origin()
@login_required
def get(user_id):
    data = dal_client.get(user_id=user_id)
    serialized_data = [
        client_schema.GetClient.construct(
            id=record.id,
            client_id=record.client_id,
            client_secret=record.client_secret,
            client_metadata=record.client_metadata,
        )
        for record in data
    ]
    if not data:
        return jsonify({"message": "No clients found"}), 404
    return client_schema.GetClients.construct(clients=serialized_data).json(), 200

@client_api_router.route("/grant-access", methods=("GET",))
@cross_origin()
@login_required
def get_grant_acces(user_id):
    data = dal_client.get_grant_access(user_id=user_id)
    serialized_data = [
        client_schema.GetGrantAccessList.construct(
            scope=token.scope,
            client_name=client.client_metadata.get('client_name'),
            expires_in=token.expires_in,
            issued_at=token.issued_at,
            client_uri=client.client_uri,
            id=token.id,
            token=token.access_token
        )
        for token, client in data
    ]
    if not data:
        return jsonify({"message": "No grant access found"}), 404
    return client_schema.GetClients.construct(access=serialized_data).json(), 200

@client_api_router.route("/grant-access/<access_id>", methods=("POST",))
@cross_origin()
@login_required
def revoke_grant_access(access_id, user_id, ):
    if not dal_client.get_grant_access_one(user_id=user_id, access_id=access_id):
        return jsonify({"message": "You are not permmited to revoke this access"}), 403
    if not dal_client.revoke_grant_access(access_id=access_id):
        return jsonify({"message": "Error occured"}), 500
    return jsonify({"message": "Successfully revoked"}), 200

@client_api_router.route("/", methods=("POST",))
@cross_origin()
@login_required
@validate()
def create(body: client_schema.CreateClient, user_id):
    is_ok, data = create_client(body, user_id)
    if not is_ok:
        return jsonify({"message": "Error accured while creating client"}), 500
    return jsonify({"message": "Successfully created"}), 201


@client_api_router.route("/<client_id>", methods=("DELETE",))
@cross_origin()
@login_required
def delete(client_id, user_id):
    is_ok = delete_client(client_id, user_id)
    if not is_ok:
        return jsonify({"message": "Error accured while deleting client"}), 500
    return jsonify({"message": "Successfully deleted"}), 201
