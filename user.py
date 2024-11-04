from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# A mock "database" of users, with email as the key and hashed passwords
mock_users_db = {
    "u@e.com": {
        "email": "u@e.com",
        "password": generate_password_hash("test")  # Hash the password
    }
}

class User(UserMixin):
    def __init__(self, email, password_hash):
        self.id = email
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def get(cls, email):
        # Fetch the user from the mock database by email
        user_data = mock_users_db.get(email)
        if user_data:
            return cls(email=user_data["email"], password_hash=user_data["password"])
        return None

    def check_password(self, password):
        # Verify the password against the stored hash
        return check_password_hash(self.password_hash, password)
