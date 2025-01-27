from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models import db  # Import db instance from models package
from routes.auth import auth  # Import auth blueprint
from routes.onboarding import onboarding  # Import onboarding blueprint
from routes.spotify import spotify
from routes.userdata import userdata
from models.user import User  # Import User model
from config import Config

app = Flask(__name__)

CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.config.from_object(Config)

db.init_app(app)

def create_tables():
    db.create_all()

with app.app_context():
    create_tables()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(onboarding, url_prefix='/ob')
app.register_blueprint(spotify, url_prefix='/spotify')
app.register_blueprint(userdata, url_prefix='/userdata')

if __name__ == '__main__':
    app.run(debug=True)
