import os
from flask import Flask
from . import db
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    # Calculate paths to frontend assets
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_folder = os.path.join(base_dir, 'frontend', 'templates')
    static_folder = os.path.join(base_dir, 'frontend', 'static')

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    # configure logging
    handler = RotatingFileHandler(os.path.join(base_dir, 'backend.log'), maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # initialize database
    db.init_db()

    # register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
