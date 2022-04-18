from datetime import datetime
from flask import jsonify, Response
from validators import user_schema
from utils.hashing import Hasher, generate_auth_token
from models.user import User, Token
from dal import dal_user
from dal import dal_tokens

def create_user(user: user_schema.CreateUser):
    password = Hasher.get_password_hash(user.password)
    user_obj = User(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        active = True,
        password = password,
    )
    return dal_user.add(user=user_obj)

def auth_user(user: User, password: str):
    is_valid_pass = Hasher.verify_password(password, user.password)
    if not is_valid_pass:
        return False, 'Password missmatch'
    previous_token = dal_tokens.get(user_id=user.id)
    if previous_token and previous_token.expire_at > datetime.utcnow():
        return True, previous_token.token
    if previous_token:
        if not dal_tokens.delete(previous_token):
            return False, "Error while token generation"
    token = Token(
        token=generate_auth_token(),
        user_id=user.id
    )
    if not dal_tokens.add(token):
        return False, 'Error while token generation'
    print(token.token)
    return True, token.token