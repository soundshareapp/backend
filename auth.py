from flask import Blueprint, jsonify, session

# Set up the blueprint for authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # Set session authenticated to True
    session['authenticated'] = True
    return jsonify({"message": "Successfully logged in!", "authenticated": True})

# Route for logout
@auth.route('/logout', methods=['POST'])
def logout():
    session['authenticated'] = False
    return jsonify({"message": "Successfully logged out", "authenticated": False})

# Route to check login status
@auth.route('/status', methods=['GET'])
def status():
    return jsonify({"authenticated": session.get('authenticated')})
    