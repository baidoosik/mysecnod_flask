from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField, BooleanField, SelectField
from wtforms.validators import Email,Required,Length, Regexp
from wtforms import ValidationError
from ..models import Role, User

class NameForm(FlaskForm):
    email = StringField('크롤링한 정보를 받을 이메일 주소를 입력해주세요.',validators=[Required(),Email()])
    submit =SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('real name',validators=[Length(0,64)])
    location = StringField('location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Edit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    user_name = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_user_name(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(use_rname=field.data).first():
            raise ValidationError('Username already in use.')

