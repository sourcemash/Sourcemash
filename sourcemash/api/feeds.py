from . import api
from sourcemash.database import db
from flask import abort
from flask.ext.restful import Resource, reqparse, fields, marshal

from datetime import datetime, date

import feedparser

from sourcemash.models import Feed

feed_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'last_updated': fields.DateTime,
}

class FeedListAPI(Resource):

    def get(self):
        return {'feeds': [marshal(feed, feed_fields) for feed in Feed.query.all()]}

class FeedAPI(Resource):

    def get(self, id):
        feed = Feed.query.get_or_404(id)
        return {'feed': marshal(feed, feed_fields)}

api.add_resource(FeedListAPI, '/feeds', endpoint='feeds')
api.add_resource(FeedAPI, '/feeds/<int:id>', endpoint='feed')