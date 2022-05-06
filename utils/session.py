from flask import session, request
from models.user import User
from flask import jsonify
from dal import dal_tokens, dal_user
import random
from config.settings import PHOTO_VERIFICATION_METHODS


def current_user():
    token = request.headers.get("Authorization")
    token_from_db = dal_tokens.get_by_token(token=token)
    if not token_from_db:
        return None
    return dal_user.get_by_id(id=token_from_db.user_id)


def generate_photo_verification_method():
    method = random.choice(PHOTO_VERIFICATION_METHODS)
    if method == PHOTO_VERIFICATION_METHODS[1]:
        return (method, random.choice(range(1, 5)))
    return (method, 1)


def login_required(func):
    def wrapper(*args, **kwargs):
        user = current_user()
        if user:
            kwargs["user_id"] = user.id
            return func(*args, **kwargs)

        return jsonify({"message": "Need to login"}), 401

    wrapper.__name__ = func.__name__
    return wrapper
