from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import Email,Required,Length

class NameForm(FlaskForm):
    email = StringField('크롤링한 정보를 받을 이메일 주소를 입력해주세요.',validators=[Required(),Email()])
    submit =SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('real name',validators=[Length(0,64)])
    location = StringField('location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Edit')