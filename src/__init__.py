import os

from flask_sqlalchemy import SQLAlchemy

from flask import Flask


# instantiate the db
db = SQLAlchemy()


# new
def create_app(config_filename=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = config_filename if config_filename else os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from src.api.ping import ping_blueprint
    from src.api.users import users_blueprint

    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
