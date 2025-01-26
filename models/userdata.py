from . import db


class UserData(db.Model):
    __tablename__ = "user_data"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    spotify_token = db.Column(db.String(255), nullable=True)
    spotify_refresh_token = db.Column(db.String(500), nullable=True)
    completed_signup = db.Column(db.Boolean, default=False, nullable=False)

    # Use string reference to avoid circular dependency
    user = db.relationship("User", back_populates="user_data")

    def __init__(
        self,
        user_id,
        username,
        name,
        avatar=None,
        spotify_token=None,
        spotify_refresh_token=None,
        completed_signup=False,
    ):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.avatar = avatar
        self.spotify_token = spotify_token
        self.spotify_refresh_token = spotify_refresh_token
        self.completed_signup = completed_signup

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def delete_data(cls, user_id):
        data = cls.query.filter_by(user_id=user_id).first()
        db.session.delete(data)
        db.session.commit()

    def update(
        self,
        username=None,
        name=None,
        avatar=None,
        spotify_token=None,
        spotify_refresh_token=None,
        completed_signup=None,
    ):
        if username is not None:
            self.username = username
        if name is not None:
            self.name = name
        if avatar is not None:
            self.avatar = avatar
        if completed_signup is not None:
            self.completed_signup = completed_signup
        if spotify_token is not None:
            self.spotify_token = spotify_token
        if spotify_refresh_token is not None:
            self.spotify_refresh_token = spotify_refresh_token
        db.session.commit()

    @classmethod
    def update_by_user_id(
        cls,
        user_id,
        username=None,
        name=None,
        avatar=None,
        spotify_token=None,
        spotify_refresh_token=None,
        completed_signup=None,
    ):
        data = cls.get_by_user_id(user_id)
        if data is not None:
            data.update(
                username=username,
                name=name,
                avatar=avatar,
                spotify_token=spotify_token,
                spotify_refresh_token=spotify_refresh_token,
                completed_signup=completed_signup,
            )
            db.session.commit()
