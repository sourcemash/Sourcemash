from . import api
from flask.ext.restful import Resource
from flask.ext.security import current_user, login_required

from sourcemash.models import Item, UserItem

from sqlalchemy import func, or_
from collections import Counter

class CategoryListAPI(Resource):

    @login_required
    def get(self):
        user_feed_ids = [feed.id for feed in current_user.subscribed]

        categories = Counter()
        unread_counts = {}

        distinct_category_1 = Item.query.with_entities(Item.category_1, func.count())   \
                                        .filter(Item.feed_id.in_(user_feed_ids))        \
                                        .group_by(Item.category_1)                      \
                                        .all()
        distinct_category_2 = Item.query.with_entities(Item.category_2, func.count())   \
                                        .filter(Item.feed_id.in_(user_feed_ids))        \
                                        .group_by(Item.category_2)                      \
                                        .all()

        for category, count in distinct_category_1 + distinct_category_2:
            if category:
                categories.update({category: count})

                read_item_count = UserItem.query.filter(UserItem.user_id==current_user.id,
                                                        or_(UserItem.category_1==category, UserItem.category_2==category), 
                                                        UserItem.unread==False).count()

                unread_counts[category] = categories[category] - read_item_count

        # Add unsubscribed items to the counts
        # Total = len(subscribed user items) + 1 unsubscribed user item
        for category in categories:
            unsubscribed_item = Item.query.filter((Item.category_1 == category) | (Item.category_2 == category))    \
                                        .filter(~Item.feed_id.in_(user_feed_ids))                                   \
                                        .first()
            if unsubscribed_item:
                categories.update({category: 1})
                unread_counts[category] += 1

        return {'categories': [{'category': category, 'count': categories[category], 
                                'unread_count': unread_counts[category]} for category in categories]}


class CategoryListAllAPI(Resource):

    def get(self):
        categories = Counter()

        distinct_category_1 = Item.query.with_entities(Item.category_1, func.count())   \
                                        .group_by(Item.category_1)                      \
                                        .all()
        
        distinct_category_2 = Item.query.with_entities(Item.category_2, func.count())   \
                                        .group_by(Item.category_2)                      \
                                        .all()

        for category, count in distinct_category_1 + distinct_category_2:
            if category:
                categories.update({category: count})

        return {'categories': [{'category': category, 'count': categories[category]} for category in categories]}


api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryListAllAPI, '/categories/all', endpoint='categories_all')

