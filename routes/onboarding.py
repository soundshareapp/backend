from flask import Blueprint, jsonify
from flask_login import current_user, login_required
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
    data = UserData.get_by_user_id(current_user.id)
    print(data)
    return jsonify({'status': 'Complete'})
