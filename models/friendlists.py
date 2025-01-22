from . import db
import uuid
from enum import Enum

class FriendRequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class FriendList(db.Model):
    __tablename__ = 'friend_list'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(FriendRequestStatus), default=FriendRequestStatus.PENDING, nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])

    def __init__(self, user_id, friend_id, status=FriendRequestStatus.PENDING):
        self.user_id = user_id
        self.friend_id = friend_id
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_friends(cls, user_id):
        return cls.query.filter_by(user_id=user_id, status=FriendRequestStatus.ACCEPTED).all()

    @classmethod
    def get_pending_requests(cls, user_id):
        return cls.query.filter_by(friend_id=user_id, status=FriendRequestStatus.PENDING).all()

    @classmethod
    def update_status(cls, request_id, new_status):
        friend_request = cls.query.get(request_id)
        if friend_request:
            friend_request.status = new_status
            db.session.commit()
            return True
        return False
