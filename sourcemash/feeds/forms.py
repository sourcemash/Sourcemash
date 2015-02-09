from wtforms import TextField, SubmitField
from wtforms.validators import ValidationError, Length

from flask_wtf import Form

import feedparser

class FeedForm(Form):
    url = TextField('Feed URL', [Length(max=120)])
    submit = SubmitField('Add Feed')

    def validate_url(form, field):
        rss_feed = feedparser.parse(field.data)
                
        if rss_feed['bozo'] == 1: # invalid feed
            raise ValidationError('URL is not a valid feed')