from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    wins = db.Column(db.Integer, autoincrement=False)
    losses = db.Column(db.Integer, autoincrement=False)

    def __init__(self, username, password, first_name, last_name, email,):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()