from . import db
import re

class UserData(db.Model):
    __tablename__ = "user_data"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), primary_key=True)
    username = db.Column(db.String(150), nullable=True, unique=True)
    name = db.Column(db.String(150), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    spotify_token = db.Column(db.String(255), nullable=True)
    spotify_refresh_token = db.Column(db.String(255), nullable=True)
    token_expires_at = db.Column(db.DateTime, nullable=True)
    completed_signup = db.Column(db.Boolean, default=False, nullable=False)

    # Use string reference to avoid circular dependency
    user = db.relationship("User", back_populates="user_data")

    def __init__(
        self,
        user_id,
        username=None,
        name=None,
        avatar=None,
        spotify_token=None,
        spotify_refresh_token=None,
        token_expires_at=None,
        completed_signup=False,
    ):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.avatar = avatar
        self.spotify_token = spotify_token
        self.spotify_refresh_token = spotify_refresh_token
        self.token_expires_at = token_expires_at
        self.completed_signup = completed_signup

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, user_id):
        return cls.query.get(user_id)
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def delete_data(cls, user_id):
        data = cls.query.filter_by(user_id=user_id).first()
        db.session.delete(data)
        db.session.commit()

    @classmethod
    def update(
        cls,
        user_id=None,
        username=None,
        name=None,
        avatar=None,
        spotify_token=None,
        spotify_refresh_token=None,
        token_expires_at=None,
        completed_signup=None,
    ):
        data = cls.get(user_id)
        if data is not None:
            if username is not None:
                data.username = username
            if name is not None:
                data.name = name
            if avatar is not None:
                data.avatar = avatar
            if spotify_token is not None:
                data.spotify_token = spotify_token
            if spotify_refresh_token is not None:
                data.spotify_refresh_token = spotify_refresh_token
            if token_expires_at is not None:
                data.token_expires_at = token_expires_at
            if completed_signup is not None:
                data.completed_signup = completed_signup
            db.session.commit()

    @classmethod
    def check_username(cls, test_username: str, user_id: str):
        if re.match("^[a-z][a-z0-9._-]{4,19}$", test_username):
            if (cls.query.filter(cls.username == test_username, cls.user_id != user_id).first() is not None):
                return {'error': 'username_taken'}
            else:
                return {'success': 'username_available'}
        else:
            return {'error': 'invalid_username'}
