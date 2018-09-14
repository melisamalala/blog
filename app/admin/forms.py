from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):

    title = StringField('Comment Title', validators=[DataRequired()])
    comment = TextAreaField('Post Of The Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')