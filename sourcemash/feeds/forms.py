from wtforms import TextField, SubmitField
from wtforms.validators import ValidationError, Length

from flask_wtf import Form

import feedparser

class FeedForm(Form):
    url = TextField('Feed URL', [Length(max=120)])
    submit = SubmitField('Add Feed')