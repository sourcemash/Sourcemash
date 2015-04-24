from . import api
from flask.ext.restful import Resource, marshal, fields
from flask.ext.security import current_user, login_required

from sourcemash.models import Item, Category, UserItem

from sqlalchemy import func


category_fields = {
  'id': fields.Integer,
  'name': fields.String(attribute='category'),
}

category_status_fields = {
  'item_count': fields.Integer,
  'unread_count': fields.Integer
}
category_status_fields = dict(category_fields, **category_status_fields)


class CategoryAPI(Resource):

    def get(self, id):
        category = Category.query.get_or_404(id)
        return {'category': marshal(category, category_fields)}


class CategoryListAPI(Resource):

    @login_required
    def get(self):
        user_feed_ids = [feed.id for feed in current_user.subscribed]

        categories = Category.query \
                             .with_entities(Category,
                                            func.count()) \
                             .join(Category.items) \
                             .filter(Item.feed_id.in_(user_feed_ids)) \
                             .group_by(Category.category) \
                             .all()

        for category, count in categories:
            read_item_count = UserItem.query \
                                .filter(UserItem.user_id==current_user.id) \
                                .join(UserItem.item) \
                                .filter(Item.cats.contains(category)) \
                                .filter(~UserItem.unread) \
                                .count()

            category.item_count = count
            category.unread_count = category.item_count - read_item_count

            unsubscribed_item = Item.query.filter(Item.cats.contains(category)) \
                                          .filter(~Item.feed_id.in_(user_feed_ids)) \
                                          .first()
            if unsubscribed_item:
                category.item_count += 1
                category.unread_count += 1

        return {'categories': [marshal(category, category_status_fields) for category, count in categories]}


class CategoryListAllAPI(Resource):

    def get(self):
        categories = Category.query.all()

        return {'categories': [marshal(category, category_fields) for category in categories]}


api.add_resource(CategoryAPI, '/categories/<int:id>', endpoint='category')
api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryListAllAPI, '/categories/all', endpoint='categories_all')
