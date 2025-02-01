from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.chatlist import ChatList, ChatMessage
from models.userdata import UserData

chat = Blueprint("chat", __name__)


@chat.route("/list", methods=["GET"])
@login_required
def get_chat_list():
    user_id = current_user.id
    chats = ChatList.get_user_chats(user_id)
    chatlist = []
    for chat in chats:
        other_user = chat.user1_id if chat.user1_id != user_id else chat.user2_id
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


@chat.route("/<id>/messages/", methods=["GET"])
@login_required
def get_chat_messages(id):
    messages = ChatList.get_chat(user1_id=id, user2_id=current_user.id).get_messages()
    return messages


@chat.route("/<id>/send/", methods=["POST"])
@login_required
def send_message(id):
    message: ChatMessage = request.json
    if (
        message["song"]
        and message["song"]["url"]
        and message["song"]["title"]
        and message["song"]["artist"]
        and message["song"]["album"]
    ):
        currentChat = ChatList.get_chat(user1_id=id, user2_id=current_user.id)
        currentChat.add_message(
            sender_id=current_user.id, song=message["song"], note=message.get("note")
        )
        return jsonify({"success": True})

    return jsonify({"success": False})

@chat.route("/<id>/delete/<message_id>/", methods=["POST"])
@login_required
def delete_message(id, message_id): 
    currentChat = ChatList.get_chat(user1_id=id, user2_id=current_user.id)
    currentChat.delete_message(message_id)
    return jsonify({"success": True})