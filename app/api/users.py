from flask import Flask
from flask.ext.restful import Api, Resource, fields, marshal, reqparse
from app import app

api = Api(app)

user_list = [
	{
		'id': 5743, 
		'email': "lhpglad@hp.org", 
	},
	{
		'id': 5744, 
		'email': "alex@shnoodles.com",  

	}
]

user_fields = {
	'email': fields.String,
	'uri': fields.Url('user')
}

class UserListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email', type = str, required = True)
		super(UserListAPI, self).__init__()

	def get(self):
		''' Show all Users '''
		return { 'users': [marshal(user, user_fields) for user in user_list] }

	def post(self):
		''' Create new User ''' 
		args = self.reqparse.parse_args()
		user = {}
		user['email'] = args.email
		user['id'] = user_list[-1]['id'] + 1
		return { 'user': user}, 201

class UserAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email', type = str, required = True)
		super(UserAPI, self).__init__()

	def get(self, id):
		''' Show User @id '''
		return { 'user': [marshal(user, user_fields) for user in user_list if user['id']==id][0] }

	def put(self, id):
		''' Edit User @id '''
		args = self.reqparse.parse_args()
		user = [ user for user in user_list if user['id']==id ][0] 
		user['email'] = args.email
		return { 'user': user }

	def delete(self, id):
		''' Destroy User @id '''
		pass

api.add_resource(UserListAPI, '/api/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/users/<int:id>', endpoint = 'user')
