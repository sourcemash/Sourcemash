from . import api, login_required
from sourcemash.database import db
from flask.ext.restful import Resource, marshal, fields, reqparse, inputs
from flask.ext.security import current_user

from sourcemash.models import Item, Category, UserItem, UserCategory

from sqlalchemy import func
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

class isUnread(fields.Raw):
    def output(self, key, category):
        try:
            unread = UserCategory.query.filter_by(user=current_user, category_id=category.id).one().unread
        except (MultipleResultsFound, NoResultFound):
            unread = True

        return unread

category_fields = {
  'id': fields.Integer,
  'name': fields.String(attribute='category'),
}

category_status_fields = {
  'unread': isUnread
}
category_status_fields = dict(category_fields, **category_status_fields)

category_status_count_fields = {
  'item_count': fields.Integer,
}
category_status_count_fields = dict(category_status_fields, **category_status_count_fields)

class CategoryAPI(Resource):

    def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('unread', type = inputs.boolean)
      super(CategoryAPI, self).__init__()

    def get(self, id):
        category = Category.query.get_or_404(id)
        return {'category': marshal(category, category_fields)}

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        category = Category.query.get_or_404(id)

        # Mark category as Read
        if args.unread != None:
            try:
                user_category = UserCategory.query.filter_by(user=current_user, category_id=category.id).one()
            except (MultipleResultsFound, NoResultFound):
                user_category = UserCategory(user=current_user, category_id=category.id)
                db.session.add(user_category)
                db.session.commit()

            # Toggle unread status
            user_category.unread = args.unread
            db.session.commit()

        return {'category': marshal(category, category_status_fields)}

class CategoryListAPI(Resource):

    def get(self):

        if not current_user.is_authenticated():
          return {'categories': []}

        user_feed_ids = [feed.id for feed in current_user.subscribed]

        categories = Category.query \
                             .with_entities(Category,
                                            func.count()) \
                             .join(Category.items) \
                             .filter(Item.feed_id.in_(user_feed_ids)) \
                             .group_by(Category.id) \
                             .all()

        for category, count in categories:

            category.item_count = count

            unsubscribed_item = Item.query.filter(Item.cats.contains(category)) \
                                          .filter(~Item.feed_id.in_(user_feed_ids)) \
                                          .first()
            if unsubscribed_item:
                category.item_count += 1

        return {'categories': [marshal(category, category_status_count_fields) for category, count in categories]}


class CategoryListAllAPI(Resource):

    def get(self):
        categories = Category.query.all()

        return {'categories': [marshal(category, category_fields) for category in categories]}


api.add_resource(CategoryAPI, '/categories/<int:id>', endpoint='category')
api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryListAllAPI, '/categories/all', endpoint='categories_all')
