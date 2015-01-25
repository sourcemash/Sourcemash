import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.models import User, Feed, Role, Item
from datetime import datetime

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: u'user%d@test.com' % n)
    password = 'password'

    @factory.post_generation
    def role(self, create, extracted, **kwargs):
        if not create:
            return

        role = extracted
        self.roles.append(role)

class FeedFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Feed
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    title = "NYTimes"
    url = "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    last_updated = datetime.min

class ItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u'Item %d Title' % n)
    link = factory.Sequence(lambda n: u"ImportantItem.com/%d" % n)
    last_updated = datetime.utcnow()
    author = 'Scott Gladstone'
    summary = 'Summary of the feed item.'
    feed_id = factory.Sequence(lambda n: n)

class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = 'user'
