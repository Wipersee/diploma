from datetime import datetime
from flask import jsonify, Response
from validators import user_schema
from utils.hashing import Hasher, generate_auth_token
from models.user import User, Token
from dal import dal_user
from dal import dal_tokens
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


def create_user(user: user_schema.CreateUser):
    password = Hasher.get_password_hash(user.password)
    user_obj = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        active=True,
        password=password,
    )
    return dal_user.add(user=user_obj)


def auth_user(user: User, body: user_schema.LoginUser):
    model = EmbeddingGenerator(
        FACE_DB_PHOTOS_PATH, FACE_DB_EMBEDDINGS_PATH, FACE_DB_FACES_PATH
    )
    username = user.username
    model.username = username
    image = Image.open(
        io.BytesIO(base64.decodebytes(bytes(body.photo.split(",")[1], "utf-8")))
    )
    # if not verification(model, image, username):
    #     return False, f"User {username} not verified"
    is_valid_pass = Hasher.verify_password(body.password, user.password)
    if not is_valid_pass:
        return False, "Password missmatch"
    previous_token = dal_tokens.get(user_id=user.id)
    if previous_token and previous_token.expire_at > datetime.utcnow():
        return True, previous_token.token
    if previous_token:
        if not dal_tokens.delete(previous_token):
            return False, "Error while token generation"
    token = Token(token=generate_auth_token(), user_id=user.id)
    if not dal_tokens.add(token):
        return False, "Error while token generation"
    print(token.token)
    return True, token.token
