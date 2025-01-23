from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from flask_login.utils import request
from models.userdata import UserData

onboarding = Blueprint('onboarding', __name__)

@onboarding.route('/status', methods=['GET'])
@login_required
def check_status():
    """
    Check if the user has completed the onboarding process
    """
    data = UserData.get_by_user_id(current_user.id)
    if data is None:
        return jsonify({'status': 'Unknown'})
    else:
        if (data.completed_signup):
            return jsonify({'status': 'Complete'})
        else:
            return jsonify({'status': 'Incomplete'})

@onboarding.route('/complete', methods=['POST'])
@login_required
def complete_onboarding():
    data = request.get_json()
    print(data)
    print(current_user.id)
    UserData.update_by_user_id(current_user.id, name=data['name'] or None, avatar=data['avatar'] or None, completed_signup=True)
    print(UserData.get_by_user_id(current_user.id))
    return jsonify({'status': 'Complete'})
