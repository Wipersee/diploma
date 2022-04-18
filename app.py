# app.state.model = EmbeddingGenerator(
#     FACE_DB_PHOTOS_PATH, FACE_DB_EMBEDDINGS_PATH, FACE_DB_FACES_PATH
# )
import os
from flask import Flask
from dal.database import db
from utils.oauth2 import config_oauth
from views.routers import bp
from views.user import user_router
from views.client import client_router
from views.oauth import oauth_router
from api.client import client_api_router
from api.user import user_api_router

def create_app(config=None):
    app = Flask(__name__)

    # load environment configuration
    if "WEBSITE_CONF" in os.environ:
        app.config.from_envvar("WEBSITE_CONF")

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith(".py"):
            app.config.from_pyfile(config)

    setup_app(app)
    return app


def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    config_oauth(app)
    app.register_blueprint(bp, url_prefix="")
    app.register_blueprint(client_router, url_prefix="")
    app.register_blueprint(oauth_router, url_prefix="")
    app.register_blueprint(user_router, url_prefix="")
    app.register_blueprint(client_api_router, url_prefix="/api/clients")
    app.register_blueprint(user_api_router, url_prefix="/api/users")

app = create_app(
    {
        "SECRET_KEY": "secret",
        "OAUTH2_REFRESH_TOKEN_GENERATOR": True,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite",
    }
)