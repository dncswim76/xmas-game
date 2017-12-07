from xmas_game import db
from enum import Enum
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        'id', db.Integer, primary_key=True)
    username = db.Column(
        'Username', db.String(50), unique=True, nullable=False)
    password = db.Column(
        'Password', db.String(120), nullable=False)
    first_name = db.Column(
        'first_name', db.String(50))
    last_name = db.Column(
        'last_name', db.String(50))

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):

        if 'authenticated' in session:
            return session['authenticated']
        else:
            return False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username


class Setting(db.Model):

    __tablename__ = 'settings'
    
    id = db.Column('id', db.Integer, primary_key=True)
    config_var = db.Column('Config_Variable', db.Text)
    value = db.Column('value', db.String(50))

    def __repr__(self):
        return self.config_var

        
class Player(db.Model):

    __tablename__ = 'players'

    class Roles(Enum):
        UNASSIGNED = 0
        NAUGHTY = 1
        NICE = 2

    id = db.Column('id', db.Integer, primary_key=True)
    role = db.Column('player_role', db.Enum(Roles), nullable=False)
    user_id = db.Column('User', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User, backref='users')
    voted_round_one = db.Column('voted_round1', db.Text)
    voted_round_two = db.Column('voted_round2', db.Text)
    voted_round_three = db.Column('voted_round3', db.Text)
    voted_round_four = db.Column('voted_round4', db.Text)


class Vote(db.Model):

    __tablename__ = 'votes'

    id = db.Column(
        'id', db.Integer, primary_key=True)
    player_id = db.Column(
        'player_id', db.Integer, db.ForeignKey('players.id'))
    voting_round = db.Column(
        'round_id', db.Integer)
    vote_id = db.Column(
        'vote_id', db.Integer, db.ForeignKey('players.id'))
