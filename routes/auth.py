from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user
from models.user import User
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Enter a valid email and password.", "authenticated": False})

    user = User.get_by_email(data.get('email'))
    if not user or not user.check_password(data.get('password')):
        return jsonify({"message": "Invalid credentials.", "authenticated": False})

    login_user(user, remember=data.get("staySignedIn"))
    return jsonify({"message": "Successfully logged in!", "authenticated": True})

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Enter a valid email and password.", "authenticated": False})

    if User.get_by_email(data.get('email')):
        return jsonify({"message": "An account with this email already exists.", "authenticated": False})

    user = User(id=str(uuid.uuid4()), email=data.get('email'), password=data.get('password'))
    user.save()
    login_user(user, remember=True)
    return jsonify({"message": "Successfully signed up!", "authenticated": True})

@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Successfully logged out", "authenticated": False})

@auth.route('/status', methods=['GET'])
def status():
    return jsonify({"authenticated": current_user.is_authenticated})
