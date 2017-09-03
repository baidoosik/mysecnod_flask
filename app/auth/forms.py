from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The Email is already used by another user ')

    def validate_username(selfs,field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('The username is already used by another user ')


class PasswordChangeForm(FlaskForm):
    present_password = PasswordField('Password', validators=[Required()])
    change_password = PasswordField('Password', validators=[
        Required(), EqualTo('change_password2', message='Passwords must match.')])
    change_password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('change password')


class EmailChangeForm(FlaskForm):
    change_email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('send new email')