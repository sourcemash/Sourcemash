from . import api
from . import is_current_user
from flask.ext.restful import Resource, marshal
from flask.ext.security import current_user, login_required

from sourcemash.models import Item
from items import item_fields

from sqlalchemy import func
from collections import Counter


class CategoryListAPI(Resource):

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


class UserCategoryListAPI(Resource):

    @login_required
    @is_current_user
    def get(self, user_id):
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


class CategoryItemListAPI(Resource):

    def get(self, category):
        """ RETURNS EMPTY LIST IF NO ARTICLES PRESENT """ 
        cat1_items = Item.query.filter_by(category_1=category).all()
        cat2_items = Item.query.filter_by(category_2=category).all()
        items = set(cat1_items + cat2_items)

        return {'items': [marshal(item, item_fields) for item in items]}

api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryItemListAPI, '/categories/<string:category>', endpoint='category')
api.add_resource(UserCategoryListAPI, '/users/<int:user_id>/categories', endpoint='user_categories')