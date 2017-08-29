from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Email,Required

class NameForm(FlaskForm):
    name= StringField('what is your name?',validators=[Required()])
    email = StringField('what is your e-mail?',validators=[Required(),Email()])
    submit =SubmitField('Submit')