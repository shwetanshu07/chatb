from chatb import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)  #autoincrement is set by default
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"
