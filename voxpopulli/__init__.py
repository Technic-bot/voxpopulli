from flask import Flask
import os

class Config:
    CLIENT_ID = os.environ.get("patreon_client_id")
    CLIENT_SECRET = os.environ.get("patreon_client_secret")
    CLIENT_TOKEN = os.environ.get("client_token")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'BAD_SECRET_KEY'

    from . import oauth
    app.register_blueprint(oauth.bp)

    return app


