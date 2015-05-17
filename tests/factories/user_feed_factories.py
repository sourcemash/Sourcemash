from tests.factories import *

from sourcemash.models import UserFeed
from user_factories import UserFactory
from feed_factories import FeedFactory


class UserFeedFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = UserFeed
    FACTORY_SESSION = db.session

    user = factory.SubFactory(UserFactory)
    feed = factory.SubFactory(FeedFactory)
    unread = True
