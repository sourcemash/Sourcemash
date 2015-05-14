import pytest
from tests.factories import user_feed_factories

@pytest.fixture()
def user_feed(request):
    return user_feed_factories.UserFeedFactory()
