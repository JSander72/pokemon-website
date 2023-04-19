from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    wins = db.Column(db.Integer, autoincrement= False)
    losses = db.Column(db.Integer, autoincrement= False)
    my_pokemon = db.relationship('MyPokemon', backref='user')

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    name = db.Column(db.String(20))
    attack = db.Column(db.Integer, autoincrement = False)
    defense = db.Column(db.Integer, autoincrement = False)
    hp = db.Column(db.Integer, autoincrement = False)
    exp = db.Column(db.Integer, autoincrement = False)
    type1 = db.Column(db.String(20))
    type2 = db.Column(db.String(20))
    poke_img = db.Column(db.String(250))
    ability1 = db.Column(db.String(20))
    ability2 = db.Column(db.String(20))
    caught = db.relationship('MyPokemon', backref='User')

    def __init__(self, id, name, attack, defense, hp , exp, type1, type2, poke_img, ability1, ability2):
        self.id = id
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.exp = exp
        self.type1 = type1
        self.type2 = type2
        self.poke_img = poke_img
        self.ability1 = ability1
        self.ability2 = ability2

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, autoincrement = False)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable = False, autoincrement = False)
    team_name = db.Column(db.String(50), nullable = False)

    def __init__(self, id, user_id, team_name):
        self.id = id
        self.user_id = user_id
        self.team_name = team_name

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class MyPokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, autoincrement = False)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.id', ondelete='CASCADE'), nullable = False, autoincrement = False)
    captured = db.relationship('Pokemon')
    pokemon = db.relationship('Pokemon', backref='captured_by')
    

    def __init__(self, user_id, poke_id):
        self.user_id = user_id
        self.poke_id = poke_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class TeamPokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable = False, autoincrement = False)
    team_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, autoincrement = False)

    def __init__(self, user_id, team_id):
        self.id = id
        self.user_id = user_id
        self.team_id = team_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

