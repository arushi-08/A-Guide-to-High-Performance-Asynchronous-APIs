import os
import random
import time
from flask import (
    Flask,
    request,
    render_template,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
)
from celery import Celery, group, chain, chord
from flask_mongoengine import MongoEngine
from project.config import config, SECRET_KEY

# creates a Flask object
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configure the redis server
app.config["CELERY_BROKER_URL"] = os.environ.get(
    "CELERY_BROKER_URL",
)
app.config["CELERY_RESULT_BACKEND"] = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
)


# Initialize Celery
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
db = MongoEngine()


def create_app(config_name=None):
    # new
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate the app
    app = Flask(__name__)
    # set config
    app.config.from_object(config[config_name])
    app.config["MONGODB_SETTINGS"] = {
        "db": "flask_celery",
    }

    # set up extensions
    db.init_app(app)
    # migrate.init_app(app, db)
    # celery.init_app(app)

    # register blueprints
    from project.api import celery_blueprint

    app.register_blueprint(celery_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
