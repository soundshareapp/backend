from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User  # Import User after initializing db to avoid circular imports
