from flask import Blueprint, current_app, abort
from flask.ext.restful import Api
from flask.ext.security import current_user

from functools import wraps

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")

def is_current_user(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.id == kwargs['user_id']:
            return abort(401)
        return func(*args, **kwargs)
    return decorated_view

import feeds
import items
import subscriptions
import users
import categories