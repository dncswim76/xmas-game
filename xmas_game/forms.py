from flask import flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    username = TextField('username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=1, max=25)])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        # validate form submission
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # try to get valid user
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


def unique_username(form, field):
    if User.query.filter(User.username == field.data).first():
        raise ValidationError('Username already exists')


class AccountCreateForm(FlaskForm):
    username = TextField('username', validators=[Length(min=4, max=25), unique_username])
    first_name = TextField('first_name', validators=[Length(min=2, max=25)])
    last_name = TextField('last_name', validators=[Length(min=2, max=25)])
    password = PasswordField('password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def validate(self):
        if len(User.query.filter(User.username == self.username.data).all()) != 0:
            flash(u'Username already taken. Choose another username.', 'failure')
            return False
        return True
