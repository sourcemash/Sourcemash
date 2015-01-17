from flask import abort
from flask.ext.restful import Api, Resource, fields, marshal, reqparse
from app import app

api = Api(app)

user_list = [
	{
		'id': 1, 
		'email': "happy@rock.com", 
	},
	{
		'id': 2, 
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
		user_list.append(user)
		return { 'user': marshal(user, user_fields)}, 201

class UserAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email', type = str, required = True)
		super(UserAPI, self).__init__()

	def get(self, id):
		''' Show User @id '''
		user = filter(lambda user: user['id']==id, user_list)
		if not user:
			abort(404)
		return { 'user': marshal(user[0], user_fields) }

	def put(self, id):
		''' Edit User @id '''
		args = self.reqparse.parse_args()
		user = filter(lambda user: user['id']==id, user_list)
		print "--", user
		if not user:
			abort(404)
		user = user[0]
		user['email'] = args.email
		return { 'user': user }

	def delete(self, id):
		''' Destroy User @id '''
		user = filter(lambda user: user['id'] == id, user_list)
		if not user:
			abort(404)
		user_list.remove(user[0])
		return {'result': True}

api.add_resource(UserListAPI, '/api/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/users/<int:id>', endpoint = 'user')
