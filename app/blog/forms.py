from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField('title',validators=[Required(), Length(1, 64)])
    content = PageDownField("what's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = TextAreaField('body',validators=[Required()])
    submit = SubmitField('Submit')