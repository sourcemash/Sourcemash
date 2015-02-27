from . import api
from sourcemash.database import db
from flask import abort
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.security import current_user, login_required

from datetime import datetime, date

import feedparser

from sourcemash.models import Feed, UserItem, Item
from sourcemash.forms import FeedForm

class isSubscribed(fields.Raw):
    def output(self, key, feed):
        if not current_user.is_authenticated():
            return False

        return feed in current_user.subscribed

class getItemCount(fields.Raw):
    def output(self, key, feed):
        return feed.items.count()

class getUnreadCount(fields.Raw):
    def output(self, key, feed):
        total_item_count = Item.query.filter_by(feed_id=feed.id).count() 
        
        if not current_user.is_authenticated():
            return total_item_count 
        
        read_item_count = UserItem.query.filter_by(user=current_user, feed_id=feed.id, unread=False).count()

        return total_item_count - read_item_count

feed_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'last_updated': fields.DateTime,
    'item_count': getItemCount,
    'unread_count': getUnreadCount,
    'subscribed': isSubscribed
}

class FeedListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                    help='No url provided')
        super(FeedListAPI, self).__init__()

    @login_required
    def get(self):
        return {'feeds': [marshal(feed, feed_fields) for feed in current_user.subscribed]}


    @login_required
    def post(self):
        args = self.reqparse.parse_args()
        form = FeedForm(obj=args)

        if not form.validate_on_submit():
            return {"errors": form.errors}, 422

        rss_feed = feedparser.parse(form.url.data)

        try:
            feed = Feed.query.filter(Feed.url==rss_feed['url']).one()
        except:

            feed = Feed(title=rss_feed['feed']['title'],
                        url=rss_feed['url'],
                        last_updated=datetime.min)

            db.session.add(feed)
            db.session.commit()

        try:
            subscription = current_user.subscribed.filter(Feed.id==feed.id).one()
            return {"errors": {"url": ["Already subscribed"]}}, 409
        except:
            current_user.subscribed.append(feed)
            db.session.commit()

        return marshal(feed, feed_fields), 201


class FeedListAllAPI(Resource):

    def get(self):
        return {'feeds': [marshal(feed, feed_fields) for feed in Feed.query.all()]}


class FeedAPI(Resource):

    def get(self, id):
        feed = Feed.query.get_or_404(id)
        return {'feed': marshal(feed, feed_fields)}


    @login_required
    def delete(self, id):
        """Unsubscribe user from feed."""

        try:
            subscription = current_user.subscribed.filter(Feed.id==id).one()
        except:
            abort(404)

        current_user.subscribed.remove(subscription)
        db.session.commit()

        return {'result': True}

api.add_resource(FeedListAPI, '/feeds', endpoint='feeds')
api.add_resource(FeedListAllAPI, '/feeds/all', endpoint='feeds_all')
api.add_resource(FeedAPI, '/feeds/<int:id>', endpoint='feed')