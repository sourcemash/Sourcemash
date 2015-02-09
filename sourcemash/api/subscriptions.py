from . import api
from sourcemash.database import db

from flask import abort, request
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.security import current_user, login_required

from sourcemash.models import Feed
from sourcemash.forms import FeedForm
import feedparser
from datetime import datetime

subscription_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.Url('frontend.feed'),
    'uri': fields.Url('api.subscription')
}

class SubscriptionListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                    help='No feed url provided')
        super(SubscriptionListAPI, self).__init__()

    @login_required
    def get(self):
        return {'subscriptions': [marshal(subscription, subscription_fields) for subscription in current_user.subscribed]}

    @login_required
    def post(self):
        form = FeedForm()

        if not form.validate_on_submit():
            return form.errors, 422

        url = form.url.data

        try:
            feed = Feed.query.filter_by(url=url).one()
        except:
            rss_feed = feedparser.parse(url)

            feed = Feed(title=rss_feed['feed']['title'],
                        url=rss_feed['url'],
                        last_updated=datetime.min)

            db.session.add(feed)
            db.session.commit()

        try:
            subscription = current_user.subscribed.filter(Feed.id==feed.id).one()
            return {"url": "Already subscribed"}, 409
        except:
            current_user.subscribed.append(feed)
            db.session.commit()

        subscription = current_user.subscribed.filter(Feed.id==feed.id).first()
        return marshal(subscription, subscription_fields), 201

class SubscriptionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mergeable', type=bool)
        super(SubscriptionAPI, self).__init__()

    @login_required
    def get(self, id):
        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        return marshal(subscription, subscription_fields)

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        if args.mergeable:
            subscription['mergeable'] = args.mergeable

        db.session.commit()

        return marshal(subscription, subscription_fields)

    @login_required
    def delete(self, id):
        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        current_user.subscribed.remove(subscription)
        db.session.commit()

        return {'result': True}

api.add_resource(SubscriptionListAPI, '/subscriptions', endpoint='subscriptions')
api.add_resource(SubscriptionAPI, '/subscriptions/<int:id>', endpoint='subscription')