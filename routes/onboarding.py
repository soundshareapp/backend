from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from models.userdata import UserData

onboarding = Blueprint("onboarding", __name__)


@onboarding.route("/status", methods=["GET"])
@login_required
def check_status():
    """
    Check if the user has completed the onboarding process
    """
    data = UserData.get(current_user.id)
    if data is None:
        return jsonify({"status": "Unknown"})
    else:
        if data.completed_signup:
            return jsonify({"status": "Complete"})
        else:
            return jsonify({"status": "Incomplete"})


@onboarding.route("/complete", methods=["POST"])
@login_required
def complete_onboarding():
    UserData.update(current_user.id, completed_signup=True)
    print(UserData.get(current_user.id))
    return jsonify({"status": "Complete"})
