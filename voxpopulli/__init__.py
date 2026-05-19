from flask import Flask

def create_app():
    app = Flask(__name__)
    # Load defaults
    app.config.from_object("voxpopulli.config.Config")
    app.config.from_envvar("VOX_SETTINGS", silent=True)
    app.secret_key = 'BAD_SECRET_KEY'

    # Initialize db function and teardown
    from . import db
    db.init_app(app)

    from . import oauth
    app.register_blueprint(oauth.bp)
    
    from . import polls
    app.register_blueprint(polls.bp)

    return app
