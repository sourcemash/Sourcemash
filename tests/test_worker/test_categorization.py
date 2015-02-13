import pytest
from sourcemash.categorize import categorize_item
from collections import Counter

class TestCategorize:

    def test_categorize_item(self, ebolaItem):
		category_dict = Counter()
		category_dict.update(ebolaItem.title.split())
		
		(cat1, cat2) = categorize_item(ebolaItem.title, ebolaItem.text, category_dict)

        category_dict = Counter()
        for word in ebolaItem['title'].split():
            if len(word) > 3:
                category_dict.update([word])
        
        (cat1, cat2) = categorize_item(ebolaItem['title'], ebolaItem['text'], category_dict)

        assert (cat1, cat2) == ("Ebola", "West")

    def test_empty_categories(self):
        category_dict = Counter() # not updated because all words in title have len(word) < 3

        (cat1, cat2) = categorize_item("Of The", "Of The Of The Of The Of The", category_dict)

        assert (cat1, cat2) == ("", "")
