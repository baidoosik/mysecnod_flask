from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

class PostForm(FlaskForm):
    title = StringField('title',validators=[Required(), Length(1, 64)])
    content = TextAreaField("what's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')