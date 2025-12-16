"""
Database Module
--------------
This module initializes the SQLAlchemy extension.
It is separated to avoid circular imports between app.py and models.py.

Variables:
    db: The SQLAlchemy instance.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
# This will be bound to the Flask app in src/app.py
db = SQLAlchemy()
