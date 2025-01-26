import requests
from flask import Blueprint, redirect, request, jsonify, session
from flask_login import login_required, current_user
from models import db
from models.userdata import UserData
from config import Config
import base64

spotify = Blueprint("spotify", __name__)


@spotify.route("/login")
@login_required
def spotify_login():
    state = current_user.id
    auth_url = (
        f"https://accounts.spotify.com/authorize"
        f"?client_id={Config.SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={Config.SPOTIFY_REDIRECT_URI}"
        f"&scope=user-read-private user-read-email"
        f"&state={state}"
    )
    return jsonify({"url": auth_url})


@spotify.route("/callback")
def spotify_callback():
    code = request.args.get("code")
    user_id = request.args.get('state')

    if not code:
        return jsonify({"error": "Authorization failed"}), 400

    # Exchange authorization code for access token
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.SPOTIFY_REDIRECT_URI,
    }
    encoded_creds = base64.b64encode(f"{Config.SPOTIFY_CLIENT_ID}:{Config.SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_creds}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(token_url, data=payload, headers=headers)
    token_info = response.json()

    if "access_token" not in token_info:
        return jsonify({"error": "Failed to retrieve access token"}), 400

    access_token = token_info["access_token"]
    refresh_token = token_info["refresh_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    profile_data = profile_response.json()

    email = profile_data.get("email")
    if not email:
        return jsonify({"error": "Failed to get user profile"}), 400

    UserData.update_by_user_id(
        user_id=user_id, spotify_token=access_token, spotify_refresh_token=refresh_token
    )

    return jsonify({"message": "Spotify connected successfully!"})


# Step 3: Refresh token endpoint
@spotify.route("/refresh-token")
def refresh_spotify_token():
    user_data = UserData.query.filter_by(user_id=current_user.id).first()
    if not user_data or not user_data.spotify_refresh_token:
        return jsonify({"error": "No refresh token found"}), 400

    refresh_payload = {
        "grant_type": "refresh_token",
        "refresh_token": user_data.spotify_refresh_token,
        "client_id": Config.SPOTIFY_CLIENT_ID,
        "client_secret": Config.SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token", data=refresh_payload
    )
    new_token_info = response.json()

    if "access_token" not in new_token_info:
        return jsonify({"error": "Failed to refresh token"}), 400

    UserData.update_by_user_id(
        current_user.id, spotify_token=new_token_info["access_token"]
    )

    return jsonify({"message": "Token refreshed successfully"})
