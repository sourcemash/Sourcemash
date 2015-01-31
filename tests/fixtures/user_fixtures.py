import pytest
from tests.factories import user_factories, role_factories, feed_factories

@pytest.yield_fixture(scope='function')
def user(request):
    feed = feed_factories.FeedFactory()
    yield user_factories.UserFactory(subscribed=[feed])