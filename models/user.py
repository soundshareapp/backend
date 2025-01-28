from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .userdata import UserData

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_data = db.relationship('UserData', back_populates='user', uselist=False, cascade="all, delete-orphan")

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        if not UserData.get(self.id):
            user_data = UserData(user_id=self.id, username="", name="", avatar="", spotify_token="", completed_signup=False)
            user_data.save()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def delete_account(cls, user_id):
        UserData.delete_data(user_id)
        user = cls.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
