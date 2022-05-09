import time
from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from models.user import db, User
from models.oauth import OAuth2Client
from utils.oauth2 import authorization, require_oauth
import requests
from dal import dal_user
from handlers.user import auth_user, login_user
from validators import user_schema
from validators.consts import LoginType
from structlog import get_logger

logger = get_logger()
bp = Blueprint("home", __name__)


@bp.route("/", methods=("POST", "GET"))
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        photo = request.form.get("photo")
        user = dal_user.get_by_name(username=username)
        token = request.form.get("token")
        if not token:
            if not user:
                return "No user found"
            body = user_schema.LoginUser.construct(
                username=username, password=password, photo=photo
            )
            is_valid, response = auth_user(
                user=user, body=body, type=LoginType.oauth.value
            )
            if not is_valid:
                return "Verification is unsuccessful"
            return render_template(
                "home.html",
                intermidiate_token=response.get("intermidiate_token"),
                verification_method=response.get("verification_method"),
                repeat=response.get("repeat"),
            )
        photos = photo.split(", ")
        body = user_schema.LoginUser.construct(
            username=username, password='', photos=photos
        )
        is_valid, response = login_user(
            user=user, token=token, photos=body.photos
        )
        if not is_valid:
            logger.error(f"User {body.username} failed in OAUTH with error {response}")
            return "Verification for real human is unsuccessful"
        logger.info(f"User {body.username} successfully loged in OAUTH")
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page + f"&token={response}")
        return redirect("/")
    return render_template("home.html")
