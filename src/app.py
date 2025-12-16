"""
Application Entry Point
----------------------
This module initializes the Flask application, configures extensions,
and registers blueprints.

Functions:
    create_app: Factory function to create and configure the Flask app.
    main: Entry point for running the application directly.
"""

from typing import Tuple
from flask import Flask, jsonify, Response
from src.db import db
from src.routes import api_blueprint
from src.auth import auth_bp
from src.config import Config

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error) -> Tuple[Response, int]:
        """Handle 404 Not Found errors."""
        return jsonify({'msg': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error) -> Tuple[Response, int]:
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        return jsonify({'msg': 'Internal server error'}), 500

    return app

def main():
    """
    Run the application in debug mode.
    """
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
