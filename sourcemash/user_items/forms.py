from wtforms import IntegerField
from wtforms.validators import ValidationError

from flask_wtf import Form

class VoteForm(Form):
    vote = IntegerField('vote')

    def validate_vote(form, field):
    	# Check vote magnitude
        if abs(field.data) > 1: 
            raise ValidationError('Vote may only be up (+1) or down (-1)')