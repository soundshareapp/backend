from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models import db  # Import db instance from models package
from routes.chat import chat
from routes.friends import friends
from routes.auth import auth  # Import auth blueprint
from routes.onboarding import onboarding  # Import onboarding blueprint
from routes.spotify import spotify
from routes.userdata import userdata
from models.user import User  # Import User model
from config import Config

app = Flask(__name__)

CORS(app, origins=Config.ALLOW_URLS, supports_credentials=True)

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
app.register_blueprint(friends, url_prefix='/friends')
app.register_blueprint(chat, url_prefix='/chat')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
