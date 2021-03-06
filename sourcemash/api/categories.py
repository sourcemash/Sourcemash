from . import api, login_required
from sourcemash.database import db
from flask.ext.restful import Resource, marshal, fields, reqparse, inputs
from flask.ext.security import current_user

from sourcemash.models import Item, Category, UserCategory

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

MIN_CATEGORY_LIMIT = 2       # Every category needs at least # entries
MIN_FEED_CATEGORY_RATIO = 5  # Category threshold increases by 1, every # feeds


class isUnread(fields.Raw):
    def output(self, key, category):
        if not current_user.is_authenticated():
            return True

        try:
            unread = UserCategory.query.filter_by(user=current_user,
                                                  category_id=category.id) \
                                       .one().unread
        except NoResultFound:
            unread = True

        return unread

category_fields = {
  'id': fields.Integer,
  'name': fields.String(attribute='category'),
  'unread': isUnread
}


class CategoryAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('unread', type=inputs.boolean)
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
            except NoResultFound:
                user_category = UserCategory(user=current_user, category_id=category.id)
                db.session.add(user_category)
                db.session.commit()

            # Toggle unread status
            user_category.unread = args.unread
            db.session.commit()

        return {'category': marshal(category, category_fields)}

class CategoryListAPI(Resource):

    def get(self):

        if not current_user.is_authenticated():
          return {'categories': []}

        user_feed_ids = [feed.id for feed in current_user.subscribed]

        categories = Category.query \
                             .with_entities(Category, func.count()) \
                             .join(Category.items) \
                             .filter(Item.feed_id.in_(user_feed_ids)) \
                             .group_by(Category.id) \
                             .all()

        min_count = current_user.subscribed.count() / MIN_FEED_CATEGORY_RATIO + MIN_CATEGORY_LIMIT

        return {'categories': [marshal(category, category_fields) for category, count in categories if count >= min_count]}


class CategoryListAllAPI(Resource):

    def get(self):
        categories = Category.query.all()

        return {'categories': [marshal(category, category_fields) for category in categories]}


api.add_resource(CategoryAPI, '/categories/<int:id>', endpoint='category')
api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryListAllAPI, '/categories/all', endpoint='categories_all')
