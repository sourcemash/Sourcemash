from . import api
from flask.ext.restful import Resource
from flask.ext.security import current_user, login_required

from sourcemash.models import Item, Category, UserItem

from sqlalchemy import func
from collections import Counter


class CategoryListAPI(Resource):

    @login_required
    def get(self):
        user_feed_ids = [feed.id for feed in current_user.subscribed]

        total_counts = Counter()
        unread_counts = {}

        categories = Category.query \
                             .with_entities(Category.category,
                                            func.count()) \
                             .join(Category.items) \
                             .filter(Item.feed_id.in_(user_feed_ids)) \
                             .group_by(Category.category) \
                             .all()

        for category, count in categories:
            total_counts.update({category: count})

            read_item_count = UserItem.query \
                                .filter(UserItem.user_id==current_user.id) \
                                .join(UserItem.item) \
                                .filter(Item.categories.contains(category)) \
                                .filter(~UserItem.unread) \
                                .count()

            unread_counts[category] = total_counts[category] - read_item_count

        # Add unsubscribed items to the counts
        # Total = len(subscribed user items) + 1 unsubscribed user item
        for category in total_counts:
            unsubscribed_item = Item.query.filter(Item.categories.contains(category)) \
                                          .filter(~Item.feed_id.in_(user_feed_ids)) \
                                          .first()
            if unsubscribed_item:
                total_counts.update({category: 1})
                unread_counts[category] += 1

        return {'categories': [{'category': category, 'count': total_counts[category], 'unread_count': unread_counts[category]} for category in total_counts]}


class CategoryListAllAPI(Resource):

    def get(self):
        categories = Category.query.with_entities(Category.category,
                                                  func.count())   \
                               .group_by(Category.category) \
                               .all()

        return {'categories': [{'category': category, 'count': count} for category, count in categories]}


api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryListAllAPI, '/categories/all', endpoint='categories_all')
