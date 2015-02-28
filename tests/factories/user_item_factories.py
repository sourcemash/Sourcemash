from tests.factories import *

from sourcemash.models import User, UserItem
from user_factories import UserFactory
from item_factories import ItemFactory


class UserItemFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = UserItem
    FACTORY_SESSION = db.session

    user = factory.SubFactory(UserFactory)
    item = factory.SubFactory(ItemFactory)


class UserItemUpvoteFactory(UserItemFactory):
    vote = 1
    item = factory.SubFactory(ItemFactory, voteSum=1)


class UserItemDownvoteFactory(UserItemFactory):
    vote = -1
    item = factory.SubFactory(ItemFactory, voteSum=-1)


class UserItemReadFactory(UserItemFactory):
	unread = False