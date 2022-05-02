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
@validate()
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
