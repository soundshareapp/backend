from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_session import Session 
from flask_cors import CORS
from auth import auth

app = Flask(__name__)

CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.config['SECRET_KEY'] = 'mysecret' # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_COOKIE_SAMESITE']='None'
app.config['SESSION_COOKIE_SECURE']='True'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

#db.create_all()

app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)