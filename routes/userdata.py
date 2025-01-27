from flask import Blueprint, redirect, request, jsonify
from flask_login import login_required, current_user
from models.userdata import UserData

userdata = Blueprint("userdata", __name__)

@userdata.route("/update", methods=["POST"])
@login_required
def update_data():
    data:dict = request.get_json()
    
    UserData.update_by_user_id(
        current_user.id,
        username=data.get('username', ''),
        name=data.get('name', ''),
        avatar=data.get('avatar', ''),
    )

    return jsonify({'updated': list(data.keys())})

@userdata.route("/<param>", methods=["GET"])
@login_required
def get_data(param):
    print(param)
    if (param != 'spotify_token' and param != 'spotify_refresh_token'):
        data = UserData.get(current_user.id)
        value = getattr(data, param)
        if value is None:
            return jsonify({"message": f"Invalid parameter: {param}"}), 400
        
        return value