from app import app
from flask import jsonify, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from datetime import datetime, date

api = Api(app)

feeds = [
	{
		'id': 1,
		'title': u'NYTimes',
		'url': u'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
		'last_updated': datetime.utcnow()
	},
	{
		'id': 2,
		'title': u'CNN',
		'url': u'http://rss.cnn.com/rss/cnn_topstories.rss',
		'last_updated': datetime.utcnow()
	}
]

feed_fields = {
    'title': fields.String,
    'url': fields.String,
    'last_updated': fields.DateTime,
    'uri': fields.Url('feed')
}

class FeedListAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, required=True,
									help='No feed title provided')
		self.reqparse.add_argument('url', type=str, required=True,
									help='No feed url provided')
		super(FeedListAPI, self).__init__()

	def get(self):
		return {'feeds': [marshal(feed, feed_fields) for feed in feeds]}

	def post(self):
		args = self.reqparse.parse_args()
		feed = {
			'id': feeds[-1]['id'] + 1,
			'title': args['title'],
			'url': args['url'],
			'last_updated': datetime.min
		}
		feeds.append(feed)
		return {'feed': marshal(feed, feed_fields)}, 201

class FeedAPI(Resource):

	def get(self, id):
		feed = filter(lambda feed: feed['id'] == id, feeds)
		if not feed:
			abort(404)
		return {'feed': marshal(feed[0], feed_fields)}

	def delete(self, id):
		feed = filter(lambda feed: feed['id'] == id, feeds)
		if not feed:
			abort(404)
		feeds.remove(feed[0])
		return {'result': True}

api.add_resource(FeedListAPI, '/api/feeds', endpoint='feeds')
api.add_resource(FeedAPI, '/api/feeds/<int:id>', endpoint='feed')