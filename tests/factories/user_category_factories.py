from tests.factories import *

from sourcemash.models import UserCategory, Category
from user_factories import UserFactory

class UserCategoryFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = UserCategory
    FACTORY_SESSION = db.session

    user = factory.SubFactory(UserFactory)
    category = Category("category")
    unread = True
