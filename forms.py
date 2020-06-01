from wtforms import Form
from wtforms import TextAreaField, SubmitField
from wtforms import validators

class PostForm(Form):
    content = TextAreaField('Post here', [
    validators.Required('No ideas?')
    ])
    submit = SubmitField('Submit')
