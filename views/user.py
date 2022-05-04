from flask import Blueprint
from flask import jsonify
from authlib.integrations.flask_oauth2 import current_token
from utils.oauth2 import require_oauth

user_router = Blueprint("user", __name__)


@user_router.route("/api/me")
@require_oauth("profile")
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username, first_name=user.first_name, email=user.email, last_name=user.last_name)
