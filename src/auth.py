"""
Authentication Module
--------------------
This module handles user authentication, including registration, login,
and token generation using JWT (JSON Web Tokens).

Blueprints:
    auth_bp: The Blueprint for authentication routes.

Routes:
    POST /auth/register: Register a new user.
    POST /auth/login: Login and receive a JWT token.
    GET /auth/me: Retrieve current user details.
"""

import datetime
from typing import Tuple, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import Blueprint, request, jsonify, current_app, Response
from src.models import User
from src.db import db

auth_bp = Blueprint('auth', __name__)

def _generate_token(user_id: int) -> str:
    """
    Generate a JWT token for a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The encoded JWT token.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

@auth_bp.route('/register', methods=['POST'])
def register() -> Tuple[Response, int]:
    """
    Register a new user.

    Expected JSON:
        username (str): Desired username.
        email (str): User's email.
        password (str): User's password.

    Returns:
        JSON: Token on success, or error message.
    """
    data: Dict[str, Any] = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON body'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'msg': 'username, email and password required'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'msg': 'User already exists'}), 409

    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=password_hash)
    
    db.session.add(user)
    db.session.commit()

    token = _generate_token(user.id)
    return jsonify({'token': token}), 201

@auth_bp.route('/login', methods=['POST'])
def login() -> Tuple[Response, int]:
    """
    Authenticate a user and return a token.

    Expected JSON:
        email (str): User's email.
        password (str): User's password.

    Returns:
        JSON: Token on success, or error message.
    """
    data: Dict[str, Any] = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON body'}), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'msg': 'email and password required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    token = _generate_token(user.id)
    return jsonify({'token': token}), 200

@auth_bp.route('/me', methods=['GET'])
def me() -> Tuple[Response, int]:
    """
    Retrieve details of the currently logged-in user.
    Requires 'Authorization: Bearer <token>' header.

    Returns:
        JSON: User details.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'msg': 'Missing token'}), 401

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'msg': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'msg': 'Invalid token'}), 401

    user = User.query.get(payload['user_id'])
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat()
    })
