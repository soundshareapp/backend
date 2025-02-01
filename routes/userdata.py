from flask import Blueprint, redirect, request, jsonify
from flask_login import login_required, current_user
from models.userdata import UserData

userdata = Blueprint("userdata", __name__)


@userdata.route("/update", methods=["POST"])
@login_required
def update_data():
    data: dict = request.get_json()

    username_check = UserData.check_username(data.get("username", ""), current_user.id)

    if username_check.get("error"):
        return jsonify({"error": username_check["error"]})

    UserData.update(
        current_user.id,
        username=data.get("username", ""),
        name=data.get("name", ""),
        avatar=data.get("avatar", ""),
    )

    return jsonify({"updated": list(data.keys())})


@userdata.route("/<params>", methods=["GET"])
@login_required
def get_multiple(params):
    params_list = params.split(",")
    data = UserData.get(current_user.id)
    result = {
        param: getattr(data, param, None)
        for param in params_list
        if param != "spotify_token" and param != "spotify_refresh_token"
    }
    return jsonify(result)


"""
@userdata.route("/get/<param>", methods=["GET"])
@login_required
def get_single(param: str):
    if param != "spotify_token" and param != "spotify_refresh_token":
        data = UserData.get(current_user.id)
        value = getattr(data, param)
        if value is None:
            return jsonify({"error": f"No value for: {param}"}), 400
        return {}
    return jsonify({"error": f"Cannot access {param}"}), 400
"""
