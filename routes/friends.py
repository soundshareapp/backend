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
    if not UserData.get_by_username(username):
        return jsonify({'error': 'User not found'})
    
    receiver_id = UserData.get_by_username(username).user_id
    sender_id = current_user.id

    if not receiver_id or receiver_id == sender_id:
        return jsonify({'error': 'Invalid User'})
    
    result = FriendList.send_friend_request(sender_id, receiver_id)
    if not result:
        return jsonify({'error': 'Request already exists'})
    return jsonify({'message': 'Friend request sent to ' + username})

@friends.route('/requests', methods=['GET'])
@login_required
def get_friend_requests():
    user_id = current_user.id
    frequests = [req.user1_id for req in FriendList.get_pending_requests(user_id)]
    reqlist = [{'id': id, 'username': UserData.get(id).username, 'name': UserData.get(id).name, 'avatar': UserData.get(id).avatar}  for id in frequests] 
    return reqlist

@friends.route('/accept/<id>', methods=['POST'])
@login_required
def accept_friend_request(id):
    if not UserData.get(id):
        return jsonify({'error': 'User not found'})
    
    FriendList.accept_friend_request(id, current_user.id)
    return jsonify({'message': 'Friend request accepted'})

@friends.route('/reject/<id>', methods=['POST'])
@login_required
def reject_friend_request(id):
    if not UserData.get(id):
        return jsonify({'error': 'User not found'})
    
    FriendList.reject_friend_request(id, current_user.id)
    return jsonify({'message': 'Friend request rejected'})