"""Creating and configuring the Flask application """
from flask import Flask
from .db import db
from .routes.auth import auth_bp
# from .routes.habits import habits_bp
# from .routes.stats import stats_bp
from dotenv import load_dotenv
import os

load_dotenv() # Load .env during development

def create_app(test_config=None):
    """Create and configure the Flask application.


    We use an application factory so we can create different app instances
    (one for production, one for testing) with isolated configurations.
    """

    app = Flask(__name__)

    # Core configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", 'dev')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (modular route groups)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Create tables for demo/dev if not using migrations
    with app.app_context():
        db.create_all()

    return app