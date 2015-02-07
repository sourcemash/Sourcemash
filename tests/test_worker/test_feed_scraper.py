import pytest
from tests.factories import feed_factories
from sourcemash.models import Item, Feed

from worker_tasks.feed_scraper import get_full_text, store_items

from datetime import datetime

class TestIngestFeeds:

    def test_ingest_feeds(self, real_feed):
        for feed in Feed.query.all():
            store_items.run(feed)
            assert feed.last_updated > datetime.min
        assert len(Item.query.all()) > 0


    def test_get_full_text(self):
        text = get_full_text("http://techcrunch.com/?p=1116410")
        assert "Co-founder Bora Celik told me at the SF Music Tech Conference" in text