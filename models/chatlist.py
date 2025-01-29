from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from . import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    messages = Column(JSON, default=[], nullable=False)

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

    def add_message(
        self,
        sender_id: str,
        songlink: str,
        rating: int,
        note: str | None,
    ):
        """Append a new message JSON object to the messages list."""
        new_message = {
            "sender_id": sender_id,
            "timestamp": datetime.now(),
            "songlink": songlink,
            "note": note,
            "rating": rating,
        }
        self.messages.append(new_message)
        db.session.commit()

    def get_messages(self):
        return self.messages

    def get_after_timestmp(self, timestamp):
        return [message for message in self.messages if message["timestamp"] > timestamp]