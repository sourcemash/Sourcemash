from . import api, login_required
from sourcemash.database import db
from flask.ext.restful import Resource, reqparse, inputs, fields, marshal
from flask.ext.security import current_user

from datetime import datetime

import feedparser
import json

from sourcemash.models import Feed, UserItem, Item

from rq import Queue
from worker import create_worker
from worker.scraper import scrape_feed_articles

REDIS_CONNECTION = create_worker()
MASH_TOPIC = "Mash"
BAD_WORDS_FILE = "./json/bad_words.json"    # From jared-mess/profanity-filter


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
        if not current_user.is_authenticated():
            return 0

        total_item_count = Item.query.filter_by(feed_id=feed.id).count()
        read_item_count = UserItem.query.filter_by(user=current_user,
                                                   feed_id=feed.id,
                                                   unread=False).count()
        return total_item_count - read_item_count

feed_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'subscribed': isSubscribed,
    'description': fields.String,
    'topic': fields.String,
    'image_url': fields.String,
    'last_updated': fields.DateTime
}

feed_status_fields = {
    'item_count': getItemCount,
    'unread_count': getUnreadCount
}
feed_status_fields = dict(feed_fields, **feed_status_fields)


class FeedListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                   help='No url provided')
        super(FeedListAPI, self).__init__()

    @login_required
    def get(self):
        return {'feeds': [marshal(feed, feed_status_fields)
                for feed in current_user.subscribed]}


    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        rss_feed = feedparser.parse(args.url)

        if rss_feed['bozo'] == 1:
            return {"errors": {"url": ["URL is not a valid feed"]}}, 422

        with open(BAD_WORDS_FILE) as data_file:
            data = json.load(data_file)
            badwords = data['badwords']
            words = rss_feed['feed']['title'].split() + \
                    rss_feed['feed']['description'].split()
            for word in words:
                if word.lower() in badwords:
                    return {"errors": {"url": ["Inappropriate feed"]}}, 403

        # Get or Create Feed
        try:
            feed = Feed.query.filter(Feed.url==rss_feed['url']).one()
        except:

            feed = Feed(title=rss_feed['feed']['title'],
                        url=rss_feed['url'],
                        description=rss_feed['feed']['description'],
                        public=Falsetopic=MASH_TOPIC,
                        last_updated=datetime.min)

            db.session.add(feed)
            db.session.commit()

            # Scrape feed (but don't fail if redis-server is down)
            try:
                q = Queue('default', connection=REDIS_CONNECTION)
                job = q.enqueue_call(func=scrape_feed_articles, args=(feed,),
                                     at_front=True, timeout=600)
            except:
                pass

        # Subscribe User
        try:
            subscription = current_user.subscribed.filter(Feed.id==feed.id).one()
            return {"errors": {"url": ["Already subscribed"]}}, 409
        except:
            current_user.subscribed.append(feed)
            db.session.commit()

        return marshal(feed, feed_status_fields), 201


class FeedListAllAPI(Resource):

    def get(self):
        feeds = Feed.query.filter(Feed.public).all()

        if current_user.is_authenticated():
            logger.info(current_user.subscribed)
            feeds += current_user.subscribed.filter(Feed.public==False).all()

        return {'feeds': [marshal(feed, feed_status_fields) for feed in feeds]}


class FeedAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('subscribed', type = inputs.boolean)
        super(FeedAPI, self).__init__()

    def get(self, id):
        feed = Feed.query.get_or_404(id)
        return {'feed': marshal(feed, feed_fields)}

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        feed = Feed.query.get_or_404(id)

        # Toggle Subscription
        if args.subscribed != None:
            if args.subscribed:
                try:
                    subscription = current_user.subscribed.filter(Feed.id==feed.id).one()
                    return {"errors": {"subscribed": ["Already subscribed."]}}, 409
                except:
                    current_user.subscribed.append(feed)
                    db.session.commit()
            else:
                try:
                    subscription = current_user.subscribed.filter(Feed.id==feed.id).one()
                    current_user.subscribed.remove(subscription)
                    db.session.commit()
                except:
                    return {"errors": {"subscribed": ["You are already unsubscribed."]}}, 409

        return {'feed': marshal(feed, feed_fields)}

api.add_resource(FeedListAPI, '/feeds', endpoint='feeds')
api.add_resource(FeedListAllAPI, '/feeds/all', endpoint='feeds_all')
api.add_resource(FeedAPI, '/feeds/<int:id>', endpoint='feed')
