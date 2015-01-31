from tests.factories import *

from app.models import User
from role_factories import RoleFactory
from feed_factories import FeedFactory

class UserFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = User
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: u'user%d@test.com' % n)
    password = 'password'
    active = True
    confirmed_at = datetime.utcnow()

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.append(role)

    @factory.post_generation
    def subscribed(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for feed in extracted:
                self.subscribed.append(feed)