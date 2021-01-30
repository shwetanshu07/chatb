from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-secret'

# SQLAlchemy - creating and initialising class object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Flask Login - creating and initialising class object
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# Intialising flask-socketio
socketio = SocketIO(app)
ROOMS = ['Lounge', 'News', 'Entertainment', 'Games', 'Movies']

from chatb import routes
