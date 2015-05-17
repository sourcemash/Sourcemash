from . import api, login_required
from sourcemash.database import db
from flask import abort
from flask.ext.restful import Resource, reqparse, inputs, fields, marshal
from flask.ext.security import current_user
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.orm.exc import NoResultFound

from feeds import feed_fields
from categories import category_fields
from sourcemash.models import Item, UserItem, Category
from sourcemash.forms import VoteForm

MAX_TRENDING_ITEMS = 10
TRENDING_ITEMS_TIMEDELTA = 14 # Days (to qualify as trending)

class getVote(fields.Raw):
    def output(self, key, item):
        if not current_user.is_authenticated():
            return 0
        try:
            vote = UserItem.query.filter_by(user=current_user, item=item).one().vote
        except NoResultFound:
            vote = 0

        return vote

class getUnreadStatus(fields.Raw):
    def output(self, key, item):
        if not current_user.is_authenticated():
            return True
        return UserItem.query.filter_by(user=current_user, item=item, unread=False).count() == 0

class getSavedStatus(fields.Raw):
    def output(self, key, item):
        if not current_user.is_authenticated():
            return False
        return UserItem.query.filter_by(user=current_user, item=item, saved=True).count() > 0

item_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'link': fields.String,
    'last_updated': fields.DateTime,
    'author': fields.String,
    'categories': fields.List(fields.Nested(category_fields), attribute="cats"),
    'voteSum': fields.Integer,
    'image_url': fields.String,
    'summary': fields.String,
    'feed': fields.Nested(feed_fields),
    'unread': getUnreadStatus,
    'saved': getSavedStatus,
    'vote': getVote
}

class ItemAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('vote', type = int, default=0)
        self.reqparse.add_argument('unread', type = inputs.boolean)
        self.reqparse.add_argument('saved', type = inputs.boolean)
        super(ItemAPI, self).__init__()

    def get(self, id):
        item = Item.query.get_or_404(id)
        return {'item': marshal(item, item_fields)}

    @login_required
    def put(self, id):
        ''' Update item vote count (& mark as read/unread)'''
        args = self.reqparse.parse_args()
        form = VoteForm(obj=args)

        if not form.validate():
            return {"errors": form.errors}, 422

        item = Item.query.get_or_404(id)

        # Reject if user has already voted
        # Check vote column of user_items table
        try:
            user_item = UserItem.query.filter_by(user=current_user, item=item).one()
        except NoResultFound:
            user_item = UserItem(user=current_user, item=item, feed_id=item.feed_id)
            db.session.add(user_item)
            db.session.commit()

        # Cast vote (if vote isn't zero or revote)
        if args.vote:
            if user_item.vote == args.vote:
                return {'errors': {'vote': ["You have already voted on this item."]}}, 422

            item.voteSum += args.vote - user_item.vote # + new vote - old vote
            user_item.vote = args.vote

        # Toggle unread status
        if args.unread != None:
            user_item.unread = args.unread

        # Toggle saved-for-later status (aka bookmarked)
        if args.saved != None:
            user_item.saved = args.saved

        user_item.last_modified = datetime.utcnow()
        db.session.commit()

        return {'item': marshal(item, item_fields)}

class SavedItemListAPI(Resource):

    @login_required
    def get(self):
        user_items = UserItem.query.filter_by(user=current_user, saved=True).all()
        return {'items': [marshal(user_item.item, item_fields) for user_item in user_items]}

class TrendingItemListAPI(Resource):

    @login_required
    def get(self):
        trending_items = UserItem.query.with_entities(UserItem.item_id, func.count())     \
                                .filter(UserItem.vote)     \
                                .filter(UserItem.last_modified > (datetime.utcnow() - timedelta(days=TRENDING_ITEMS_TIMEDELTA))) \
                                .group_by(UserItem.item_id)        \
                                .order_by(desc(func.count(UserItem.item_id)))

        trending_items = trending_items[:MAX_TRENDING_ITEMS]

        return {'items': [marshal(Item.query.get(id), item_fields) for id, count in trending_items]}


class FeedItemListAPI(Resource):

    def get(self, feed_id):
        return {'items': [marshal(item, item_fields) for item in Item.query.filter_by(feed_id=feed_id).all()]}

class CategoryItemListAPI(Resource):

    @login_required
    def get(self, category_id):
        user_feed_ids = [feed.id for feed in current_user.subscribed]
        category = Category.query.get_or_404(category_id)

        items = Item.query.filter(Item.categories.contains(category.category)) \
                          .filter(Item.feed_id.in_(user_feed_ids)) \
                          .all()

        unsubscribed_item = Item.query.filter(Item.categories.contains(category.category))     \
                                      .filter(~Item.feed_id.in_(user_feed_ids))                               \
                                      .first()

        if unsubscribed_item:
            items.append(unsubscribed_item)

        return {'items': [marshal(item, item_fields) for item in items]}


class CategoryItemListAllAPI(Resource):

    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        items = Item.query.filter(Item.categories.contains(category.category)).all()
        return {'items': [marshal(item, item_fields) for item in items]}

api.add_resource(ItemAPI, '/items/<int:id>', endpoint='item')
api.add_resource(SavedItemListAPI, '/items/saved', endpoint='saved_items')
api.add_resource(TrendingItemListAPI, '/items/trending', endpoint='trending_items')
api.add_resource(FeedItemListAPI, '/feeds/<int:feed_id>/items', endpoint='feed_items')
api.add_resource(CategoryItemListAPI, '/categories/<int:category_id>/items', endpoint='category_items')
api.add_resource(CategoryItemListAllAPI, '/categories/<int:category_id>/items/all', endpoint='category_items_all')
