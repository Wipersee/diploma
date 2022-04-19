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

bp = Blueprint("home", __name__)


def current_user():
    if "id" in session:
        uid = session["id"]
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@bp.route("/", methods=("POST", "GET"))
def home():
    # HERE PHOTOGRAPHS
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        photo = request.form.get("photo")
        user = dal_user.get_by_name(username=username)
        if not user:
            return "No user found"
        body = user_schema.LoginUser.construct(username=username, password=password, photo=photo)
        is_valid, token = auth_user(user=user, body=body)
        if not is_valid:
            return "Unatorized"

        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page+f"&token={token}")
        return redirect("/")
    user = current_user()
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []
    return render_template("home.html", user=user, clients=clients)


@bp.route("/logout")
def logout():
    del session["id"]
    return redirect("/")
