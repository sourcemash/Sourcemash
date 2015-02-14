import pytest
from worker_tasks.scraper import _get_full_text

class TestScraper:

    def test_get_full_text(self):
        text = _get_full_text("http://techcrunch.com/?p=1116410")
        assert "Co-founder Bora Celik told me at the SF Music Tech Conference" in text