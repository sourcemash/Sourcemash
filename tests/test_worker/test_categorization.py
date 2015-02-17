import pytest
from worker_tasks.categorize import Categorizer
from collections import Counter

class TestCategorize:

    def test_categorize_item(self, ebolaItem):
        categorizer = Categorizer()
        
        categorizer.parse_title_categories([ebolaItem.title])
        
        (cat1, cat2) = categorizer.categorize_item(ebolaItem.title, ebolaItem.text)

        assert (cat1, cat2) == ("Ebola", "new cases")

    
    def test_empty_categories(self):
        categorizer = Categorizer()

        (cat1, cat2) = categorizer.categorize_item("Of The", "Of The Of The Of The Of The")

        assert (cat1, cat2) == ("", "")


    def test_parse_title_categories(self, item):
        categorizer = Categorizer()
        categorizer.parse_title_categories([item.title])

        assert categorizer.title_categories['Item'] == 1

    def test_reset_title_categories(self, item):
        categorizer = Categorizer()
        categorizer.parse_title_categories([item.title])

        assert categorizer.title_categories['Item'] == 1

        categorizer.reset_title_categories()

        # Counts should have been set back to zero
        assert categorizer.title_categories['Item'] == 1