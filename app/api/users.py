from flask import abort
from flask.ext.restful import Api, Resource, fields, marshal, reqparse
from flask.ext.security import login_user
from app import app, db
from app.models import User, user_datastore

api = Api(app)

user_fields = {
    'email': fields.String,
    'uri': fields.Url('user')
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
		user = user_datastore.create_user(email=args.email, password=args.password)
		role = user_datastore.find_or_create_role('user')
		if not user:
			abort(400)
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
        user_datastore.delete_user(user)
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return {'result': True}

api.add_resource(UserListAPI, '/api/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/users/<int:id>', endpoint = 'user')
