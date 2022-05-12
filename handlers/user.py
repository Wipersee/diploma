from datetime import datetime
from flask import jsonify, Response
from validators import user_schema
from utils.hashing import Hasher, generate_auth_token
from models.user import User, Token, UnauthorizedLogins
from dal import dal_user
from dal import dal_tokens
from utils.validation import EmbeddingGenerator, verification
from config.settings import (
    FACE_DB_PHOTOS_PATH,
    FACE_DB_EMBEDDINGS_PATH,
    FACE_DB_FACES_PATH,
    PHOTO_VERIFICATION_METHOD_EYE,
    PHOTO_VERIFICATION_METHOD_MOUTH,
)
import numpy as np
from PIL import Image
import io
from uuid import uuid4
from mimetypes import guess_extension, guess_type
import base64
from structlog import get_logger
from validators.consts import LoginType
from cal.cache_driver import cache_driver
from utils.session import generate_photo_verification_method
from blinking_detector import BlinkingDetector
from mouth_detector import MouthDetector
import pickle
from utils.embedding import facenet_model

logger = get_logger()


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
    if not dal_user.add(user=user_obj):
        return False, "Can not create user"
    user = dal_user.get_by_name(username=user.username)
    token = Token(token=generate_auth_token(), user_id=user.id)
    if not dal_tokens.add(token):
        return False, "Error while token generation"
    return True, token.token


def update_user(user: user_schema.PutUser, user_id: str):
    if not dal_user.update(user=user, user_id=user_id):
        return False, "Error while updating user"
    return True, "User info updated successfully"


def update_user_password(password: user_schema.UserPassword, user):
    is_valid_pass = Hasher.verify_password(password.old_password, user.password)
    if not is_valid_pass:
        return False, "Old password is wrong"
    hashed_password = Hasher.get_password_hash(password.password)
    if not dal_user.update_password(password=hashed_password, user_id=user.id):
        return False, "Error while updating user password"
    return True, "Password successfully changed"


def auth_user(
    user: User, body: user_schema.LoginUser, type: str = LoginType.default.value
):
    model = facenet_model
    username = user.username
    model.username = username
    image = Image.open(
        io.BytesIO(base64.decodebytes(bytes(body.photo.split(",")[1], "utf-8")))
    )
    verified, results = verification(model, image, username)
    if not verified:
        try:
            filename = f"{username}_{uuid4()}"
            file_extension = guess_extension(guess_type(body.photo)[0])
            img = Image.open(
                io.BytesIO(base64.decodebytes(bytes(body.photo.split(",")[1], "utf-8")))
            )
            img.save(f"store/unauthorized_logins/{filename}{file_extension}")
            unauthorized_login = UnauthorizedLogins(
                user_id=user.id,
                type=type,
                similarity=str(max(results)),
                photo_filename=f"{filename}{file_extension}",
            )
            if not dal_user.add_unauthorized_logins(
                unauthorized_login=unauthorized_login
            ):
                return False, f"User {username} not verified"
            return (
                False,
                f"User {username} not verified. Photo saved for security reasons",
            )
        except Exception as e:
            logger.exception(
                f"Exception while saving unauthorized image for {username}"
            )
            return False, f"User {username} not verified"
    is_valid_pass = Hasher.verify_password(body.password, user.password)
    if not is_valid_pass:
        return False, "Password missmatch"
    intermidiate_token = generate_auth_token()
    method, count = generate_photo_verification_method()
    response = {
        "intermidiate_token": intermidiate_token,
        "verification_method": method,
        "repeat": count,
    }
    cache_method = pickle.dumps(response)
    if not cache_driver.update(key=f"user.{user.id}.auth.method", value=cache_method):
        return False, "Error while intermidiate token generation"
    return True, response


def login_user(user, token, photos):
    verification_conditions = pickle.loads(
        cache_driver.get(f"user.{user.id}.auth.method")
    )
    repeat = verification_conditions.get("repeat")
    if not verification_conditions.get("intermidiate_token") == token:
        return False, "Invalid token. Try again from first step"
    images = [
        Image.open(io.BytesIO(base64.decodebytes(bytes(photo.split(",")[1], "utf-8"))))
        for photo in photos
    ]

    if (
        verification_conditions.get("verification_method")
        == PHOTO_VERIFICATION_METHOD_EYE
    ):
        detector = BlinkingDetector(0.25, 3, user.username, facenet_model)
        if not detector.check(num_blinks=repeat, images=images):
            filename = f"{user.username}_{uuid4()}"
            file_extension = guess_extension(guess_type(photos[0])[0])
            img = Image.open(
                io.BytesIO(base64.decodebytes(bytes(photos[0].split(",")[1], "utf-8")))
            )
            img.save(f"store/unauthorized_logins/{filename}{file_extension}")
            unauthorized_login = UnauthorizedLogins(
                user_id=user.id,
                type="DEFAULT",
                similarity=str(1.0),
                photo_filename=f"{filename}{file_extension}",
            )
            if not dal_user.add_unauthorized_logins(
                unauthorized_login=unauthorized_login
            ):
                return False, f"User {user.username} not verified. Conditions does not satisfied"
            return (
                False,
                f"User {user.username} not verified. Conditions does not satisfied. Photo saved for security reasons",
            )

    elif (
        verification_conditions.get("verification_method")
        == PHOTO_VERIFICATION_METHOD_MOUTH
    ):
        detector = MouthDetector(0.79, user.username, facenet_model)
        if not detector.check(
            num_mouth_opens=repeat,
            images=images,
        ):
            filename = f"{user.username}_{uuid4()}"
            file_extension = guess_extension(guess_type(photos[0])[0])
            img = Image.open(
                io.BytesIO(base64.decodebytes(bytes(photos[0].split(",")[1], "utf-8")))
            )
            img.save(f"store/unauthorized_logins/{filename}{file_extension}")
            unauthorized_login = UnauthorizedLogins(
                user_id=user.id,
                type="DEFAULT",
                similarity=str(1.0),
                photo_filename=f"{filename}{file_extension}",
            )
            if not dal_user.add_unauthorized_logins(
                unauthorized_login=unauthorized_login
            ):
                return False, f"User {user.username} not verified. Conditions does not satisfied"
            return (
                False,
                f"User {user.username} not verified. Conditions does not satisfied. Photo saved for security reasons",
            )
    previous_token = dal_tokens.get(user_id=user.id)
    if previous_token and previous_token.expire_at > datetime.utcnow():
        return True, previous_token.token
    if previous_token:
        if not dal_tokens.delete(previous_token):
            return False, "Error while token generation"
    token = Token(token=generate_auth_token(), user_id=user.id)
    if not dal_tokens.add(token):
        return False, "Error while token generation"
    return True, token.token
