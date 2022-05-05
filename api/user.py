import time
from flask_pydantic import validate
from flask import Blueprint, jsonify
from utils.session import login_required
from handlers.user import create_user, auth_user, update_user, update_user_password
from validators import user_schema
from dal import dal_user, dal_tokens
from utils.validation import EmbeddingGenerator
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
from flask_cors import cross_origin
from io import BytesIO

logger = structlog.get_logger()

user_api_router = Blueprint("api_user", __name__)


@user_api_router.route("/", methods=["GET"])
@cross_origin()
@login_required
def get_user_info(user_id):
    user = dal_user.get_by_id(id=user_id)
    if not user:
        return jsonify({"message": "No user found"}), 404
    user_data = user_schema.GetUser.construct(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )
    return user_data.json(), 200


@user_api_router.route("/unauthorized-logins/", methods=["GET"])
@cross_origin()
@login_required
def get_unauthorized_logins(user_id):
    unauth_logins = dal_user.get_unauth_by_user_id(id=user_id)
    serialized_data = []
    for record in unauth_logins:
        try:
            with open(
                f"store/unauthorized_logins/{record.photo_filename}", "rb"
            ) as image_file:
                data = base64.b64encode(image_file.read())
        except FileNotFoundError:
            logger.error(
                f"File {record.photo_filename} not found for user with id {user_id}"
            )
            data = ""
        serialized_data.append(
            user_schema.GetUnauth.construct(
                date=record.date,
                type=record.type,
                similarity=record.similarity,
                photo=data,
            )
        )

    if not unauth_logins:
        return jsonify({"message": "No unauthorized logins found"}), 404
    return user_schema.GetUnauths.construct(logins=serialized_data).json(), 200


@user_api_router.route("/unauth-dashboard/", methods=["GET"])
@cross_origin()
@login_required
def get_unauthorized_logins_dashboard(user_id):
    unauth_logins_pie = dal_user.get_unauth_by_user_id_for_pie(id=user_id)
    unauth_logins_line = dal_user.get_unauth_by_user_id_for_line(id=user_id)
    return_data = user_schema.GetDash.construct(
        line=[
            user_schema.GetLine.construct(date=line[0], value=line[1])
            for line in unauth_logins_line
        ],
        pie=[
            user_schema.GetPie.construct(type=line[0], value=line[1])
            for line in unauth_logins_pie
        ],
    ).json()
    return return_data, 200


@user_api_router.route("/", methods=["PUT"])
@cross_origin()
@login_required
@validate()
def update_user_info(body: user_schema.PutUser, user_id):
    user = dal_user.get_by_id(id=user_id)
    logger.info(f"User with id {user_id} trying to update personal info")
    if not user:
        logger.error(f"User with id {user_id} not found")
        return jsonify({"message": "No user found"}), 404
    status, error = update_user(user=body, user_id=user_id)
    if not status:
        logger.exception(f"Error occured while updating user info with id {user_id}")
        return jsonify({"message": error}), 500
    logger.info(f"Successfully updated user info with id {user_id}")
    return body.json(), 200


@user_api_router.route("/password/", methods=["PUT"])
@cross_origin()
@login_required
@validate()
def update_user_password_api(body: user_schema.UserPassword, user_id):
    user = dal_user.get_by_id(id=user_id)
    logger.info(f"User with id {user_id} trying to change password")
    if not user:
        logger.error(f"User with id {user_id} not found")
        return jsonify({"message": "No user found"}), 404
    status, error = update_user_password(password=body, user=user)
    if not status:
        logger.exception(f"Error occured while changing user password with id {user_id}")
        return jsonify({"message": error}), 500
    logger.info(f"Successfully changed password for user with id {user_id}")
    return jsonify({"message": error}), 200


@user_api_router.route("/", methods=["POST"])
@validate()
def signup(body: user_schema.CreateUser):
    if dal_user.get_by_name(username=body.username):
        return jsonify({"message": "Username is not free"}), 409
    is_ok, message = create_user(user=body)
    if not is_ok:
        return jsonify({"message": message}), 500
    return jsonify({"message": message}), 200


@user_api_router.route("/login", methods=["POST"])
@cross_origin()
@validate()
def login(body: user_schema.LoginUser):
    user = dal_user.get_by_name(username=body.username)
    logger.info(f"User {body.username} trying to login")
    if not user:
        logger.error(f"User {body.username} not found for login")
        return jsonify({"message": "No user found"}), 404
    is_valid, token = auth_user(user=user, body=body)
    if not is_valid:
        logger.error(f"User {body.username} failed auth flow with error {token}")
        return jsonify({"message": token}), 401
    logger.info(f"User {body.username} successfully loged in")
    return jsonify({"message": token}), 200


@user_api_router.route("/logout/", methods=["POST"])
@cross_origin()
@login_required
def logout(user_id):
    token = dal_tokens.get(user_id=user_id)
    dal_tokens.delete(token)
    return jsonify({"message": "Logged out"}), 200


@user_api_router.route("/auth-photos/", methods=["POST"])
@cross_origin()
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
    logger.info(f"User with id {user_id} trying to update personal auth photos")
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
    logger.info(f"User with id {user_id} successfully updated personal auth photos")
    return jsonify({"message": "Successfully trained model."}), 200
