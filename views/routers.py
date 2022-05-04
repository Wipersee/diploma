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
from handlers.user import auth_user
from validators import user_schema
from validators.consts import LoginType

bp = Blueprint("home", __name__)

@bp.route("/", methods=("POST", "GET"))
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        photo = request.form.get("photo")
        print(request.form)
        user = dal_user.get_by_name(username=username)
        if not user:
            return "No user found"
        body = user_schema.LoginUser.construct(
            username=username, password=password, photo=photo
        )
        is_valid, token = auth_user(user=user, body=body, type=LoginType.oauth.value)
        if not is_valid:
            return "Verification is unsuccessful"

        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page + f"&token={token}")
        return redirect("/")
    return render_template("home.html")

