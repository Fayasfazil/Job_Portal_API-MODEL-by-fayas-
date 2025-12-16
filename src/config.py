"""
Configuration Module
-------------------
This module handles the configuration settings for the Flask application.
It uses environment variables to secure sensitive information like secret keys
and database URLs.

Classes:
    Config: Base configuration class.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration class.

    Attributes:
        SECRET_KEY (str): Secret key for signing session cookies and JWTs.
        SQLALCHEMY_DATABASE_URI (str): Database connection string.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable modification tracking to save memory.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/job_portal'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
