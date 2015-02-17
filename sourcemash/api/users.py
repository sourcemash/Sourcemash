from . import api
from sourcemash.database import db

from flask import abort
from flask.ext.restful import Resource, fields, marshal, reqparse
from flask.ext.security import login_user, RegisterForm

from sourcemash.database import user_datastore
from sourcemash.models import User

user_fields = {
    'email': fields.String,
    'uri': fields.Url('api.user')
}

class UserListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str, required = True)
        self.reqparse.add_argument('password', type = str, required = True)
        super(UserListAPI, self).__init__()

    def get(self):
        ''' Show all Users '''
        return { 'users': [marshal(user, user_fields) for user in User.query.all()] }

    def post(self):
        ''' Create new User ''' 
        args = self.reqparse.parse_args()
        form = RegisterForm(obj=args)

        if not form.validate_on_submit():
            return {"errors": form.errors}, 422

        user = user_datastore.create_user(email=args.email, password=args.password)
        role = user_datastore.find_or_create_role('user')
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
        login_user(user)
        db.session.commit()
        return { 'user': marshal(user, user_fields)}, 201

class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str, required = True)
        super(UserAPI, self).__init__()

    def get(self, id):
        ''' Show User @id '''
        user = user_datastore.get_user(id)
        if not user:
            abort(404)
        return { 'user': marshal(user, user_fields) }

    def put(self, id):
        ''' Edit User @id '''
        args = self.reqparse.parse_args()
        user = user_datastore.get_user(id)
        if not user:
            abort(404)
        user.email = args.email
        db.session.commit()
        return { 'user': marshal(user, user_fields) }

    def delete(self, id):
        ''' Destroy User @id '''
        user = user_datastore.get_user(id)
        if not user:
            abort(404)
        user_datastore.delete_user(user)
        db.session.delete(user)
        db.session.commit()
        return {'result': True}

api.add_resource(UserListAPI, '/users', endpoint = 'users')
api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')
