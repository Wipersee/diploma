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

client_api_router = Blueprint("api_client", __name__)

@client_api_router.route("/", methods=("POST",))
# @login_required
@validate()
def create(body: client_schema.CreateClient):
    data = request.get_json()
    user = current_user()
    if not create_client(data, user):
        return jsonify({"message": "Error accured while creating client"}), 500
    return jsonify({"message":"Client created successfully"}), 201