from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models import db  # Import db instance from models package
from routes.auth import auth  # Import auth blueprint
from models.user import User  # Import User model

app = Flask(__name__)

CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.config['SECRET_KEY'] = 'mysecret'  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = 'True'

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
