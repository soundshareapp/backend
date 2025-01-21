import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import db instance from models/__init__.py

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Use UUID for user ID
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the provided password with the stored hash."""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get(cls, email):
        """Fetch user from the database by email."""
        return cls.query.filter_by(email=email).first()

    def save(self):
        """Save the user to the database."""
        db.session.add(self)
        db.session.commit()
