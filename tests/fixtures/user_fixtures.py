import pytest
from tests.factories import user_factories, role_factories, feed_factories

@pytest.yield_fixture(scope='function')
def user(request):
    role = role_factories.RoleFactory()
    feed = feed_factories.FeedFactory()
    yield user_factories.UserFactory(roles=[role], subscribed=[feed])