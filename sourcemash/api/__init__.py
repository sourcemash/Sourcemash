from flask import Blueprint
from flask.ext.restful import Api

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")

from functools import wraps
from flask.ext.security import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated():
            return {"errors": "Not logged in."}, 401
        return f(*args, **kwargs)
    return decorated_function

import feeds
import items
import users
import categories
