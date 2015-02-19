from . import api
from flask.ext.restful import Resource
from flask.ext.security import current_user, login_required

from sourcemash.models import Item

from sqlalchemy import func
from collections import Counter


class CategoryListAPI(Resource):

    @login_required
    def get(self):
        user_feed_ids = [feed.id for feed in current_user.subscribed]

        categories = Counter()

        distinct_category_1 = Item.query.with_entities(Item.category_1, func.count())   \
                                        .filter(Item.feed_id.in_(user_feed_ids))        \
                                        .group_by(Item.category_1)                      \
                                        .all()
        distinct_category_2 = Item.query.with_entities(Item.category_2, func.count())   \
                                        .filter(Item.feed_id.in_(user_feed_ids))        \
                                        .group_by(Item.category_2)                      \
                                        .all()

        for category, count in distinct_category_1 + distinct_category_2:
            categories.update({category: count})

        return {'categories': [{'category': category, 'count': categories[category]} for category in categories]}


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
            categories.update({category: count})

        return {'categories': [{'category': category, 'count': categories[category]} for category in categories]}


api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryListAllAPI, '/categories/all', endpoint='categories_all')

