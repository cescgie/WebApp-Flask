from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class PaperSubmissionForm(Form):
    authors = StringField('Authors', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[DataRequired()])
