from . import api, login_required
from sourcemash.database import db

from flask import abort
from flask.ext.restful import Resource, fields, marshal, reqparse, inputs
from flask.ext.security import login_user, logout_user, RegisterForm, current_user

from sourcemash.security import user_datastore
from sourcemash.models import User

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'show_suggested_content': fields.Boolean
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
        return { 'user': marshal(user, user_fields)}, 201

class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str)
        self.reqparse.add_argument('show_suggested_content', type = inputs.boolean)
        super(UserAPI, self).__init__()

    def get(self):
        return { 'user': marshal(current_user, user_fields) }

    @login_required
    def put(self):
        args = self.reqparse.parse_args()

        # Edit user email
        if args.email != None:
            current_user.email = args.email

        # Toggle unsubscribed content status
        if args.show_suggested_content != None:
            current_user.show_suggested_content = args.show_suggested_content

        db.session.commit()

        return { 'user': marshal(current_user, user_fields) }

    @login_required
    def delete(self):
        user_datastore.delete_user(current_user)
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return {'result': True}


api.add_resource(UserListAPI, '/users', endpoint = 'users')
api.add_resource(UserAPI, '/user', endpoint = 'user')

