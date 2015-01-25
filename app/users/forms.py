from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, ValidationError

from app import user_datastore

_default_field_labels = {
    'email': 'Email Address',
    'password': 'Password',
    'retype_password': 'Retype Password',
    'remember_me': 'Remember Me',
    'login': 'Login',
    'register': 'Register',
}

def get_form_field_label(key):
    return _default_field_labels.get(key, '')

class UniqueUser(object):
    def __init__(self, message="User exists"):
        self.message = message

    def __call__(self, form, field):
        if user_datastore.find_user(email=field.data):
            raise ValidationError(self.message)

validators = {
    'email': [
        Required(),
        Email(),
        UniqueUser(message='Email address is associated with '
                           'an existing account')
    ],
    'password': [
        Required(),
        Length(min=6),
        EqualTo('password_confirm', message='Passwords must match'),
        Regexp(r'[A-Za-z0-9@#$%^&+=]',
               message='Password contains invalid characters')
    ]
}