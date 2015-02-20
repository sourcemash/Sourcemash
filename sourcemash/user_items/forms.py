from wtforms import IntegerField
from wtforms.validators import NumberRange, ValidationError

from flask_wtf import Form

class VoteForm(Form):
    vote = IntegerField('vote', [NumberRange(-1, 1, 'Vote may only be up (+1) or down (-1)')])