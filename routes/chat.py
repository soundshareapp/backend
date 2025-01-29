from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.chatlist import ChatList
from models.userdata import UserData

chat = Blueprint('chat', __name__)

@chat.route('/list', methods=['GET'])
@login_required
def get_chat_list():
    user_id = current_user.id
    chats = ChatList.get_user_chats(user_id)
    chatlist = []
    for chat in chats:
        other_user = chat.user1_id if chat.user1_id != user_id else chat.user2_id;
        chat_data = {
            'id': chat.id,
            'userdata': {
                'id': other_user,
                'name': UserData.get(other_user).name,
                'username': UserData.get(other_user).username,
                'avatar': UserData.get(other_user).avatar,
            },
            'timestamp': chat.get_last_timestamp(),
        }
        chatlist.append(chat_data)
    return chatlist

@chat.route('/<id>/messages/', methods=['GET'])
@login_required
def get_chat_messages(id):
    messages = ChatList.get_chat(user1_id=id, user2_id=current_user.id).get_messages()
    return messages

