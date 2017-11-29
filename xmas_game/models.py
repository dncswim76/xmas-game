from xmas_game import db
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
    phone_number = db.Column(
        'phone_number', db.String(50))

    def __init__(self, username, password):
        self.username = username
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

    def check_password(self, pasword):
        return check_password_hash(self.pasword, password)

    def __repr__(self):
        return self.username


class Settings(db.Model):

    __tablename__ = 'settings'
    
    id = db.Column('id', db.Integer, primary_key=True)
    config_var = db.Column('Config_Variable', db.Text)
    value = db.Column('value', db.String(50))

    def __repr__(self):
        return self.config_var


class Round(db.Model):

    __tablename__ = 'rounds'

    id = db.Column(
        'id', db.Integer, primary_key=True)
    round_name = db.Column(
        'round_name', db.String(50))

    
class Vote(db.Model):

    __tablename__ = 'votes'

    id = db.Column(
        'id', db.Integer, primary_key=True)
    player = db.Column(
        'player_id', db.Integer, db.ForeignKey('players.id'))
    voting_round = db.Column(
        'round_id', db.Integer, db.ForeignKey('rounds.id'))
    vote = db.Column(
        'votee_id', db.Integer, db.ForeignKey('players.id'))

        
class Player(db.Model):

    __tablename__ = 'players'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('User', db.Integer, db.ForeignKey('users.id'))
    player_role = db.Column('player_role', db.String(10))
