from datetime import datetime, timezone
import math
import random
from sqlalchemy import Column, Integer, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.mutable import MutableList
from . import db
from typing import TypedDict


class SongData(TypedDict):
    title: str
    artist: str
    album: str
    cover: str
    url: str


class ChatMessage(TypedDict):
    id: str
    sender_id: str
    timestamp: datetime
    song: SongData
    note: str | None
    rating: int | None


alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"


def gen_message_id():
    return "".join(random.choices(alphabet, k=16))


class ChatList(db.Model):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    messages = Column(MutableList.as_mutable(JSON), default=[], nullable=False)

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_chat_pair"),
    )

    # Relationships to fetch user details
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

    @classmethod
    def get_chat(cls, user1_id, user2_id):
        """Retrieve an existing chat or create a new one."""
        chat = cls.query.filter(
            ((cls.user1_id == user1_id) & (cls.user2_id == user2_id))
            | ((cls.user1_id == user2_id) & (cls.user2_id == user1_id))
        ).first()
        if not chat:
            chat = cls(user1_id=user1_id, user2_id=user2_id, messages=[])
            db.session.add(chat)
            db.session.commit()
        return chat

    def get_user_chats(user_id):
        return (
            ChatList.query.filter_by(user1_id=user_id).all()
            + ChatList.query.filter_by(user2_id=user_id).all()
        )

    def get_last_timestamp(self):
        if len(self.messages) > 0:
            return self.messages[0]["timestamp"]
        else:
            return None

    def add_message(
        self,
        sender_id: str,
        song: SongData,
        note: str | None = None,
    ):
        """Append a new message JSON object to the messages list."""
        new_message: ChatMessage = {
            "id": gen_message_id(),
            "sender_id": sender_id,
            # Converting timestamp to milliseconds for frontend
            "timestamp": math.floor(datetime.now(timezone.utc).timestamp() * 1000),
            "song": song,
            "rating": None,
            "note": note,
        }
        self.messages.insert(0, new_message)
        db.session.commit()

    def delete_message(self, message_id):
        self.messages = [
            message for message in self.messages if message["id"] != message_id
        ]
        db.session.commit()

    def get_messages(self) -> list[ChatMessage]:
        return self.messages

    def get_message(self, message_id) -> ChatMessage | None:
        for message in self.messages:
            if message["id"] == message_id:
                return message
        return None

    def rate_message(self, message_id, rating):
        for message in self.messages:
            if message["id"] == message_id:
                message["rating"] = rating

        flag_modified(self, "messages")
        db.session.commit()

    def get_after_timestmp(self, timestamp):
        return [
            message for message in self.messages if message["timestamp"] > timestamp
        ]
