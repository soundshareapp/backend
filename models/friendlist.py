from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from . import db

class FriendList(db.Model):
    __tablename__ = "friendlists"

    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Request sender
    user2_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Request receiver
    status = Column(String, default="pending")  # 'pending', 'accepted', or 'rejected'

    # Define relationships to User
    user1 = relationship(
        "User", foreign_keys=[user1_id], backref="friend_requests_sent"
    )
    user2 = relationship(
        "User", foreign_keys=[user2_id], backref="friend_requests_received"
    )

    # Enforce unique friend pairs
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_friend_pair"),
    )

    @classmethod
    def send_friend_request(cls, sender_id, receiver_id):
        """Send a friend request."""
        # Ensure request doesn't already exist
        existing_request = cls.query.filter_by(
            user1_id=sender_id, user2_id=receiver_id
        ).first()
        existing_request_reverse = cls.query.filter_by(
            user1_id=receiver_id, user2_id=sender_id
        ).first()

        if not existing_request and not existing_request_reverse:
            request = cls(user1_id=sender_id, user2_id=receiver_id)
            db.session.add(request)
            db.session.commit()
            return request

        if (existing_request and existing_request.status == "accepted") or (
            existing_request_reverse and existing_request_reverse.status == "accepted"
        ):
            return "request_accepted"

        return "request_exists"

    @classmethod
    def accept_friend_request(cls, sender_id, receiver_id):
        """Accept a friend request."""
        request = cls.query.filter_by(
            user1_id=sender_id, user2_id=receiver_id, status="pending"
        ).first()
        if request:
            request.status = "accepted"
            db.session.commit()
            return request
        return None

    @classmethod
    def reject_friend_request(cls, sender_id, receiver_id):
        """Reject a friend request."""
        request = cls.query.filter_by(
            user1_id=sender_id, user2_id=receiver_id, status="pending"
        ).first()
        if request:
            request.status = "rejected"
            db.session.commit()
            return request
        return None

    @classmethod
    def get_friends(cls, user_id):
        """Retrieve all accepted friends for a user."""
        friends_as_user1 = cls.query.filter_by(
            user1_id=user_id, status="accepted"
        ).all()
        friends_as_user2 = cls.query.filter_by(
            user2_id=user_id, status="accepted"
        ).all()

        # Combine and return friend IDs
        friend_ids = [f.user2_id for f in friends_as_user1] + [
            f.user1_id for f in friends_as_user2
        ]
        return friend_ids

    @classmethod
    def get_pending_requests(cls, user_id):
        """Retrieve all pending friend requests for a user."""
        requests = cls.query.filter_by(user2_id=user_id, status="pending").all()
        return requests

    @classmethod
    def delete_user(cls, user_id):
        """Delete all friend associations for a user."""
        requests = cls.query.filter_by(user1_id=user_id).all() + cls.query.filter_by(user2_id=user_id).all()
        for request in requests:
            db.session.delete(request)