from flask import Blueprint, jsonify, session, request
from flask_login import login_user, logout_user, UserMixin, LoginManager, current_user
from user import User

# Set up the blueprint for authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if data is None or len(data) == 0 or data.get('email') is None or data.get('password') is None:
        return jsonify({"message": "Application error. Please try again later or <a class='errorcontact' href='https://github.com/soundshareapp/' target='_blank'>contact us.</a>", "authenticated": False})

    if data.get('email') is "" or data.get('password') is "":
        return jsonify({"message": "Enter a valid email and password to proceed.", "authenticated": False})

    user = User.get(data.get('email'))

    if user is None:
        return jsonify({"message": "No account found for this email. Please sign up.", "authenticated": False})

    if not user.check_password(data.get('password')):
        return jsonify({"message": "Email and password do not match.", "authenticated": False})

    login_user(user, remember=data.get("staySignedIn"))
    return jsonify({"message": "Successfully logged in!", "authenticated": True})

# Route for logout
@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Successfully logged out", "authenticated": False})

# Route to check login status
@auth.route('/status', methods=['GET'])
def status():
    return jsonify({"authenticated": current_user.is_authenticated})
