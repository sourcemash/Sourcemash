from tests.factories import *

from sourcemash.models import UserCategory
from user_factories import UserFactory
from category_factories import CategoryFactory


class UserCategoryFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = UserCategory
    FACTORY_SESSION = db.session

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    unread = True
