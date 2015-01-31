import pytest
from tests.factories import feed_factories

@pytest.yield_fixture(scope='function')
def feed(request):
    yield feed_factories.FeedFactory()

@pytest.yield_fixture(scope='function')
def real_feed(request):
    yield feed_factories.NYTFeedFactory()