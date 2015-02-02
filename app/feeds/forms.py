from wtforms import Form, TextField, SubmitField, validators

class AddFeedForm(Form):
    feed_url = TextField('Feed URL', [validators.Length(max=120)])
    submit = SubmitField('Add Feed')