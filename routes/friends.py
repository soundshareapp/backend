import time
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.userdata import UserData
from models.friendlist import FriendList

friends = Blueprint('friends', __name__)

@friends.route('/get', methods=['GET'])
@login_required
def get_friends():
    user_id = current_user.id
    friends = FriendList.get_friends(user_id)
    friendlist = [{'id': friend, 'username': UserData.get(friend).username, 'name': UserData.get(friend).name} for friend in friends] 
    return friendlist

@friends.route('/send/<username>', methods=['POST'])
@login_required
def send_friend_request(username):
    receiver_id = UserData.get_by_username(username).id
    sender_id = current_user.id
    if not receiver_id:
        return jsonify({'error': 'User not found'})
    FriendList.send_friend_request(sender_id, receiver_id)
    return jsonify({'message': 'Friend request sent'})

@friends.route('/requests', methods=['GET'])
@login_required
def get_friend_requests():
    user_id = current_user.id
    frequests = FriendList.get_pending_requests(user_id)
    reqlist = [{'id': req, 'username': UserData.get(req).username, 'name': UserData.get(req).name} for req in frequests] 
    return reqlist