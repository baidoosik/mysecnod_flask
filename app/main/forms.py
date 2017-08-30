from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Email,Required

class NameForm(FlaskForm):
    email = StringField('크롤링한 정보를 받을 이메일 주소를 입력해주세요.',validators=[Required(),Email()])
    submit =SubmitField('Submit')