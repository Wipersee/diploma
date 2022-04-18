from flask import Blueprint
from utils.oauth2 import authorization
from utils.session import current_user
from flask import Blueprint, request, url_for
from flask import render_template, redirect
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from models.user import User
from utils.oauth2 import authorization, require_oauth

oauth_router = Blueprint("oauth", __name__)


@oauth_router.route("/oauth/authorize", methods=["GET", "POST"])
def authorize():
    user = current_user()
    # if user log status is not true (Auth server), then to log it in
    if not user:
        return redirect(url_for("home.home", next=request.url))  # HERE LOGIN
    if request.method == "GET":
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template("authorize.html", user=user, grant=grant)
    if not user and "username" in request.form:
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
    if request.form["confirm"]:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)


@oauth_router.route("/oauth/token", methods=["POST"])
def issue_token():
    return authorization.create_token_response()


@oauth_router.route("/oauth/revoke", methods=["POST"])
def revoke_token():
    return authorization.create_endpoint_response("revocation")
