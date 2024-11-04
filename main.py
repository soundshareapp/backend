from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_session import Session 
from flask_cors import CORS
from auth import auth
from flask_login import LoginManager

from user import User

app = Flask(__name__)

CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.config['SECRET_KEY'] = 'mysecret' # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_COOKIE_SAMESITE']='None'
app.config['SESSION_COOKIE_SECURE']='True'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

sess = Session(app)

app.register_blueprint(auth, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    return User.get(id)

if __name__ == '__main__':
    app.run(debug=True)