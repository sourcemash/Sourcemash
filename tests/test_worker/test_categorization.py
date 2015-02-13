import pytest
from sourcemash.categorize import categorizeItem
from collections import Counter

class TestCategorize:

    def test_categorize_item(self, ebolaItem):
		category_dict = Counter()
		category_dict.update(ebolaItem.title.split())
		
		(cat1, cat2) = categorize_item(ebolaItem.title, ebolaItem.text, category_dict)

		assert (cat1, cat2) == ("Ebola", "West")