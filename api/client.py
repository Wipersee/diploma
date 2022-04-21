import time
from flask import Blueprint, jsonify, request
from flask_pydantic import validate
from werkzeug.security import gen_salt
from dal.database import db
from models.oauth import OAuth2Client
from utils.session import split_by_crlf, current_user
from utils.session import login_required
from handlers.client import create_client
from validators import client_schema
from dal import dal_client
import json

client_api_router = Blueprint("api_client", __name__)


@client_api_router.route("/", methods=("GET",))
@login_required
@validate()
def get(user_id):
    data = dal_client.get(user_id=user_id)
    serialized_data = [
        client_schema.GetClient.construct(
            client_id=record.client_id,
            client_secret=record.client_secret,
            client_metadata=record.client_metadata,
        ).json()
        for record in data
    ]
    if not data:
        return jsonify({"message": "No clients found"}), 404
    return jsonify(serialized_data), 200


@client_api_router.route("/", methods=("POST",))
@login_required
@validate()
def create(body: client_schema.CreateClient, user_id):
    is_ok, data = create_client(body, user_id)
    if not is_ok:
        return jsonify({"message": "Error accured while creating client"}), 500
    return jsonify(data), 201
