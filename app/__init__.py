"""Creating and configuring the Flask application """
from flask import Flask
from .db import db

def create_app():
    """Create and configure the Flask application.


    We use an application factory so we can create different app instances
    (one for production, one for testing) with isolated configurations.
    """

    app = Flask(__name__)

    # Initialize extensions
    db.init_app(app)