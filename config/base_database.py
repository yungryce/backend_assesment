#!/usr/bin/python3
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy database object
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the SQLAlchemy database with the Flask application.

    :param app: Flask application instance
    """
    db.init_app(app)

    # Create the tables if they don't exist
    with app.app_context():
        db.create_all()