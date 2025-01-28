from flask import Blueprint, redirect, request, jsonify
from flask_login import login_required, current_user
from models.userdata import UserData
 
userdata = Blueprint("userdata", __name__)
 
@userdata.route("/update", methods=["POST"])
@login_required
def update_data():
    data:dict = request.get_json()
 
    username_check = UserData.check_username(data.get('username', ''), current_user.id)
    
    if username_check.get('error'):
        return jsonify({"error" : username_check['error']})
 
    UserData.update_by_user_id(
        current_user.id,
        username=data.get('username', ''),
        name=data.get('name', ''),
        avatar=data.get('avatar', ''),
    )
 
    return jsonify({'updated': list(data.keys())})
 
@userdata.route("/get_multiple/<params>", methods=["GET"])
@login_required
def get_multiple_data(params):
    params_list = params.split(',')
    data = UserData.get(current_user.id)
    result = {}
    for param in params_list:
        value = getattr(data, param, None)
        if value is None:
            return jsonify({"message": f"Invalid parameter: {param}"}), 400
        result[param] = value

    return jsonify(result)

@userdata.route("/<param>", methods=["GET"])
@login_required
def get_data(param:str):
    if (param != 'spotify_token' and param != 'spotify_refresh_token'):
        data = UserData.get(current_user.id)
        value = getattr(data, param)
        if value is None:
            return jsonify({"message": f"Invalid parameter: {param}"}), 400
        return value
    