import time
from flask_pydantic import validate
from flask import Blueprint, jsonify, request
from flask import render_template, redirect
from werkzeug.security import gen_salt
from dal.database import db
from models.oauth import OAuth2Client
from utils.session import split_by_crlf, current_user
from utils.session import login_required
from handlers.user import create_user, auth_user
from validators import user_schema
from dal import dal_user, dal_tokens
from utils.validation import EmbeddingGenerator, verification
from config.settings import (
    FACE_DB_PHOTOS_PATH,
    FACE_DB_EMBEDDINGS_PATH,
    FACE_DB_FACES_PATH,
)
import os
import shutil
from PIL import Image
import io
import structlog
from uuid import uuid4
from mimetypes import guess_extension, guess_type
import base64

logger = structlog.get_logger()

user_api_router = Blueprint("api_user", __name__)


@user_api_router.route("/", methods=["POST"])
@validate()
def signup(body: user_schema.CreateUser):
    if dal_user.get_by_name(username=body.username):
        return jsonify({"message": "Username is not free"}), 409
    if not create_user(user=body):
        return jsonify({"message": "Error while creating user"}), 500
    return body.json(), 204


@user_api_router.route("/login", methods=["POST"])
@validate()
def login(body: user_schema.LoginUser):
    user = dal_user.get_by_name(username=body.username)
    if not user:
        return jsonify({"message": "No user found"}), 404
    is_valid, token = auth_user(user=user, body=body)
    if not is_valid:
        return jsonify({"message": token}), 401
    return jsonify({"message": token}), 200


@user_api_router.route("/logout", methods=["POST"])
@login_required
def logout(user_id):
    token = dal_tokens.get(user_id=user_id)
    dal_tokens.delete(token)
    return jsonify({"message": "Logged out"}), 200


@user_api_router.route("/auth-photos", methods=["POST"])
@login_required
@validate()
def load_photos(
    body: user_schema.UserPhotos,
    user_id,
):
    model = EmbeddingGenerator(
        FACE_DB_PHOTOS_PATH, FACE_DB_EMBEDDINGS_PATH, FACE_DB_FACES_PATH
    )
    user = dal_user.get_by_id(id=user_id)
    username = user.username
    model.username = username
    dir_name = f"store/face_db_photos/{username}"
    try:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        for photo in body.photos:
            file_extension = guess_extension(guess_type(photo)[0])
            img = Image.open(
                io.BytesIO(base64.decodebytes(bytes(photo.split(",")[1], "utf-8")))
            )
            img.save(f"store/face_db_photos/{username}/{str(uuid4())}{file_extension}")
    except Exception as e:
        logger.error(f"Photo unpacking failed reason: {e}")
        return jsonify({"message": "Error while image unpacking"}), 500

    try:
        model.setup()
    except Exception as e:
        logger.error(f"Model training failed reason: {e}")
        return jsonify({"message": "Error while model training"}), 500
    return jsonify({"message": "Successfully trained model."}), 200
