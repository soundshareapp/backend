from . import db

class UserData(db.Model):
    __tablename__ = 'user_data'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    completed_signup = db.Column(db.Boolean, default=False, nullable=False)
    spotify_token = db.Column(db.String(255), nullable=True)

    # Use string reference to avoid circular dependency
    user = db.relationship('User', back_populates='user_data')

    def __init__(self, user_id, name, avatar=None, completed_signup=False, spotify_token=None):
        self.user_id = user_id
        self.name = name
        self.avatar = avatar
        self.completed_signup = completed_signup
        self.spotify_token = spotify_token

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.get(user_id)
