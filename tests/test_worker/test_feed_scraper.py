import pytest
from tests.factories import feed_factories
from sourcemash.models import Item, Feed

from worker_tasks.scraper import Scraper

from datetime import datetime

class TestScraper:

    def test_get_full_text(self):
        scraper = Scraper()

        text = scraper.get_full_text("http://techcrunch.com/?p=1116410")
        assert "Co-founder Bora Celik told me at the SF Music Tech Conference" in text


    def test_parse_title_categories(self, item):
        scraper = Scraper()
        scraper.parse_title_categories([item.title])

        assert scraper.title_categories['Item'] == 1

    def test_reset_title_categories(self, item):
        scraper = Scraper()
        scraper.parse_title_categories([item.title])

        assert scraper.title_categories['Item'] == 1

        scraper.reset_title_categories()

        # Counts should have been set back to zero
        assert scraper.title_categories['Item'] == 1