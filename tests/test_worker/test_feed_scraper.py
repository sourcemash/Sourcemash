import pytest
from tests.factories import feed_factories
from sourcemash.models import Item, Feed

from worker_tasks.feed_scraper import store_items

from datetime import datetime

class TestIngestFeeds:

    def test_ingest_feeds(self, real_feed):
        for feed in Feed.query.all():
            store_items.run(feed)
            assert feed.last_updated > datetime.min
        assert len(Item.query.all()) > 0